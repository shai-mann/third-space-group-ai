"""
This is where database interface code goes
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..",'.env.dev')

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

def initialize_database():
    conn = connect_db()
    if conn:
        try:
            # First, drop existing tables to reset the database
            execute_sql_file(conn, 'src/postgres/drop-db.sql')
            # Assuming 'execute_sql_file' is a function that takes a connection
            # and the path to an SQL file, and executes the SQL commands in the file.
            execute_sql_file(conn, 'src/postgres/schema.sql')
            database = Database()
            users = database.getUsers()
            hobbies = database.getHobbies()
            users_id = database.getUsersIds()

            for user in users:
                print(user)
            
                

            for hobby in hobbies:
                print(hobby)
            
            
            print("Database initialized successfully.")

            for user_id in users_id:
                print(user_id[0])
                
        except Exception as e:
            print(f"Error initializing the database: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")

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

class Database():
    """
    Stores methods related to fetching information from the database.

    This is not be the best way to actually construct this, but I'm just writing it down 
    here so I can at least have some methods to work off of when I write Ford-Fulkerson.
    """

    def getUsers(self):
        query = "SELECT * FROM users;"
        return execute_query(query)
    

    def getUsersIds(self):
        query = "SELECT id FROM users;"
        return execute_query(query)
    
    def getHobbies(self):
        query = "SELECT * FROM hobbies;"
        return execute_query(query)

    
    def getUserHobbies(self, user_id):
        query = """
        SELECT h.*
        FROM hobbies h
        JOIN user_hobbies uh ON h.id = uh.hobby
        WHERE uh."user" = %s;
        """
        return execute_query(query, (user_id,))

    
    def getUserFriends(self, user_id):
        query = """
        SELECT u.*
        FROM users u
        JOIN user_friends uf ON u.id = uf.friend
        WHERE uf."user" = %s;
        """
        return execute_query(query, (user_id,))

    
    def getGroups(self):
        pass
    
    def getGroupMembers(self):
        pass


