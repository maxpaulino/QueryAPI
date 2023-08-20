from flask import jsonify, send_from_directory
from completions import generate_sql_code
from settings import app, conn
import pyodbc
import yaml
import os

# ROUTES


# /.well-known/ai-plugin.json

@app.route('/.well-known/ai-plugin.json')
def serve_manifest():
    return send_from_directory(os.path.dirname(__file__), 'ai-plugin.json') 


# /openapi.yaml

@app.route('/openapi.yaml')
def serve_openapi_yaml():
    with open(os.path.join(os.path.dirname(__file__), 'openapi.yaml'), 'r') as f:
        yaml_data = f.read()
    yaml_data = yaml.load(yaml_data, Loader=yaml.FullLoader)
    return jsonify(yaml_data)


# /logo.png

@app.route('/logo.png')
def serve_logo():
    return send_from_directory(os.path.dirname(__file__), 'logo.png', mimetype='image/png') 

# /getquery/<string:nl_query>

@app.route('/getquery/<string:nl_query>', methods=['GET'])
def get_query(nl_query):
    if not nl_query:
        return {"error": "Empty query provided"}, 400

    try:
        with conn.cursor() as cursor:
            sql_query = generate_sql_code(nl_query)
            app.logger.info(sql_query)
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return jsonify(rows_to_dict_list(cursor, result))

    except pyodbc.Error as e:
        return {"error": str(e)}, 500

    except Exception as e:
        return {"error": str(e)}, 500

 
def rows_to_dict_list(cursor, rows):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
