# Imports

import os
import openai
import pyodbc 
from flask import Flask

# Settings and configurations

PORT = 5000

app = Flask(__name__)

conn = pyodbc.connect(
    "Driver={SQL Server};"
    f"Server={os.getenv('SQL_SERVER')};"
    f"Database={os.getenv('SQL_DATABASE')};"
    f"UID={os.getenv('SQL_USERNAME')};"
    f"PWD={os.getenv('SQL_PASSWORD')};"
    f"PORT={os.getenv('SQL_PORT')};"
)

openai.api_key = os.environ.get('OPENAI_API_KEY')


# Optimized