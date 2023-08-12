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
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    f"PORT={os.getenv('DB_PORT')};"
)

openai.api_key = os.environ.get('OPENAI_API_KEY')


# Optimized