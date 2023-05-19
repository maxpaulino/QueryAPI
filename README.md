# QueryAPI

This is a Flask application that generates SQL queries based on natural language queries using OpenAI's GPT-3.5 Turbo model. The generated SQL queries are executed on a SQL Server database using pyodbc.

## Setup

1. Install the required dependencies listed in the `requirements.txt` file.

2. Create a virtual environment (optional but recommended).

3. Rename the `.env.example` file to `.env` and provide the necessary
   configuration values:

   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `DB_SERVER`: The SQL Server host or IP address.
   - `DB_NAME`: The name of the database.
   - `DB_USERNAME`: The username to connect to the database.
   - `DB_PASSWORD`: The password to connect to the database.
   - `USERNAME`: The username to connect to the API.
   - `PASSWORD`: The password to connect to the API.
   - `JWT_SECRET_PASSWORD`: The secret password to connect to the API?.

4. Run the Flask application by executing the following command:

   ```bash
   python app.py
   ```

   The application will start running on http://localhost:5000.

## API Endpoint

### **GET /getquery/{nl_query}**

This endpoint accepts a natural language query string (nl_query) as a parameter
and returns the result of the executed SQL query. The nl_query parameter should
be URL-encoded if it contains spaces or special characters.

Example: http://localhost:5000/getquery/what are the top 5 customers?

Response (JSON):

```json
{
  "data": [
    { "CustomerName": "Customer 1", "TotalOrders": 10 },
    { "CustomerName": "Customer 2", "TotalOrders": 8 },
    { "CustomerName": "Customer 3", "TotalOrders": 5 },
    { "CustomerName": "Customer 4", "TotalOrders": 4 },
    { "CustomerName": "Customer 5", "TotalOrders": 3 }
  ]
}
```

- Errors
  - If an empty query is provided:

```json
{
  "error": "Empty query provided"
}
```

- If there is an error executing the SQL query:

```json
{
  "error": "Error message"
}
```
