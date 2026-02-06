import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

# FORCE LOAD .ENV FROM PARENT FOLDER
base_dir = Path(__file__).resolve().parent.parent
env_file = base_dir / '.env'
load_dotenv(dotenv_path=env_file, encoding='utf-8')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'), 
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"[ERROR] CONNECTION ERROR: {err}")
        return None

def fetch_query(query, params=None):
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"[ERROR] FETCH ERROR: {err}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"[ERROR] EXECUTE ERROR: {err}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()