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


class Database():
    """
    Stores methods related to fetching information from the database.

    This is not be the best way to actually construct this, but I'm just writing it down 
    here so I can at least have some methods to work off of when I write Ford-Fulkerson.
    """

    def getUsers(self):
        pass
    
    def getHobbies(self):
        pass
    
    def getUserHobbies(self):
        pass
    
    def getUserFriends(self):
        pass
    
    def getGroups(self):
        pass
    
    def getGroupMembers(self):
        pass


