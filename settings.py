# Imports

import os
import openai
import pyodbc 
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Settings and configurations

PORT = 5000

app = Flask(__name__)

conn = pyodbc.connect(
    "Driver={SQL Server};"
    f"Server={os.getenv('SQL_SERVER')};"
    f"Database={os.getenv('SQL_DATABASE')};"
    f"UID={os.getenv('SQL_USERNAME')};"
    f"PWD={os.getenv('SQL_PASSWORD')};"
)

openai.api_key = os.getenv('OPENAI_API_KEY')


# Optimized