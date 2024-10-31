from flask import Flask, jsonify
from dotenv import load_dotenv
import pyodbc
import os

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    try:
        conn_str = f"DRIVER={{Pervasive ODBC Interface}};SERVERNAME={os.getenv('SERVERNAME')};DBQ={os.getenv('DBQ')};UID={os.getenv('UID')};PWD={os.getenv('PWD')};"
        connection = pyodbc.connect(conn_str)
        return connection
    except pyodbc.Error as e:
        app.logger.error(f"Database connection error: {e}")
        return None

@app.route('/api/v1')
def home():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MACHINE, WC_NAME FROM WORKCENTERS")
        rows = cursor.fetchall()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except pyodbc.Error as e:
        app.logger.error(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
