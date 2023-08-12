from settings import openai, conn

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
