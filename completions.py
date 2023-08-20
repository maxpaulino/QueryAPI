from settings import openai, conn, app


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

    # Fetch all table names
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        schema += "Table " + table_name + ':\n'

        # Fetch columns for the current table
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = cursor.fetchall()

        for column in columns:
            schema += f"- {column[0]}: {column[1]}\n"
        schema += '\n'

    app.logger.info(schema)
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
