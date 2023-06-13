# Imports

from flask import Flask, jsonify, request
import pyodbc
import openai
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime

# This code initializes a Flask application and loads environment variables
# using load_dotenv(). It also sets the OpenAI API key from the environment variable
# named OPENAI_API_KEY. Additionally, it establishes a connection to a SQL Server
# database using pyodbc module with the server name, database name, username, and 
# password provided as environment variables.

app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

conn = pyodbc.connect(
    "Driver={SQL Server};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
)

def_password = os.getenv('PASSWORD')
def_username = os.getenv('USERNAME')

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  

jwt = JWTManager(app)

# This code defines a function that connects to a database and retrieves the
# schema of all its tables. It first creates an empty string called "schema" 
# and a cursor object to interact with the database. Then, it retrieves the 
# names of all tables in the database using the "tables()" method provided by 
# the cursor object. For each table, it retrieves the names of all columns using 
# the "columns()" method and appends them to the "schema" string. Finally, it 
# returns the "schema" string containing the schema for all tables in the database.

def get_schema():
    schema = ""
    cursor = conn.cursor()
    tables = cursor.tables()
    for table in tables:
        schema += table.table_name + '\n'
        for row in cursor.columns(table=table.table_name):
            schema += row.column_name + '\n'
        schema += '\n'
    return schema

# This function generates SQL code based on a user-specified query, using Open 
# AI's GPT-3 natural language processing model. It starts by opening a conversation 
# between the system and user, where the system provides a schema and prompts the 
# user to provide an SQL query. The user-supplied query is then used to generate 
# SQL code using the GPT-3 model. The generated SQL code is returned by the function

def generate_sql_code(query):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": get_schema() +
                        "\n\n" +
                        "Let's think step by step. " +
                        "Use the schema above to create an SQL Query. " +
                        "You are only allowed to output the SQL Query."},
            {"role": "user", "content": query}
        ],
        temperature=0.75
    )
    sql_code = completion.choices[0].message.content
    return sql_code

# This is a Flask route for user login authentication. The code receives a POST
# request with username and password data in JSON format. If the credentials
# are invalid, a 401 error is returned, otherwise, an access token is created
# and returned with a 200 success status code.

@app.route('/login', methods=['POST'])
def login():

    username = request.json.get('username')
    password = request.json.get('password')

    if username != def_username or password != def_password:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)

    return jsonify({'access_token': access_token}), 200

# This code defines a Flask route for an endpoint that is protected with JWT authentication. 
# The endpoint returns a JSON response containing a message and the current user's 
# identity.

@app.route('/protected', methods=['GET'])
@jwt_required()  
def protected():

    current_user = get_jwt_identity()

    return jsonify({'message': 'Protected endpoint', 'user': current_user}), 200

# This code defines a route '/getquery' that accepts a natural language query
# string as a parameter. If the query is empty, it returns an error. Otherwise, 
# it generates SQL code based on the natural language query, executes it on
# the database connected by pyodbc, and returns the fetched result as a JSON
# object. If pyodbc throws an error, it returns a 500 error with the error message. 
# Otherwise, it returns a 200 status code with the result or error message.

@app.route('/getquery/<string:nl_query>', methods=['GET'])
def get_query(nl_query):
    if not nl_query:
        return {"error": "Empty query provided"}, 400

    try:
        with conn.cursor() as cursor:
            sql_query = generate_sql_code(nl_query)
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return {"data": result}

    except pyodbc.Error as e:
        return {"error": str(e)}, 500

    except Exception as e:
        return {"error": str(e)}, 500

# Main Function

if __name__ == '__main__':
    app.run(debug=True)

