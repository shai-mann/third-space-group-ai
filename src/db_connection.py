import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..",'.env')

load_dotenv(dotenv_path=dotenv_path)

# Database parameters
db_params = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'), 
    'password': os.environ.get('DB_PASSWORD'),   
    'host': os.environ.get('DB_HOST'),   
    'port': os.environ.get('DB_PORT'),  
}

# Establishing a connection to the database
def connect_db():
    try:
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(query, args=None):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, args)
                if cur.description:  # Check if it's a SELECT query
                    return cur.fetchall()
                conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()
    return None

# Function to execute SQL file
def execute_sql_file(conn, filepath):
    with open(filepath, 'r') as file:
        sql_script = file.read()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_script)
            conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback the transaction on error
        print(f"Error executing SQL script: {e}")
        raise e

def check_table_exists(conn, table_name):
    """
    Check if a table exists in the database.
    """
    query = """
    SELECT EXISTS (
        SELECT FROM pg_catalog.pg_tables 
        WHERE  schemaname != 'pg_catalog' AND 
               schemaname != 'information_schema' AND 
               tablename  = %s
    );
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        return cur.fetchone()[0]