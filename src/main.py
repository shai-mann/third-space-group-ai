import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
db_params = {
    'dbname': 'postgres', 
    'user': 'postgres',    
    'password': '12345',   
    'host': 'localhost',   
    'port': '5432'         
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

def main():
    # Connect to the database
    conn = connect_db()
    if conn:
        print("Connected to the database successfully.")
        conn.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
