"""
This is where database interface code goes
"""
import psycopg2
from psycopg2 import sql
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

def initialize_database():
    conn = connect_db()
    if conn:
        try:
            if should_update_schema(conn):
                execute_sql_file(conn, 'src/postgres/schema.sql')
                print("Schema updated successfully.")
            else:
                print("No schema update needed.")

            # Post-initialization tasks
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


def should_update_schema(conn):
    """
    Determine whether the schema needs to be updated by checking the existence of multiple tables.
    """
    tables_to_check = ['users', 'hobbies', 'user_hobbies', 'user_friends', 'groups', 'group_members', 'user_affinities']
    for table in tables_to_check:
        if not check_table_exists(conn, table):
            return True
    return False

def drop_database():
    conn = connect_db()
    if conn:
        try:
            execute_sql_file(conn, 'src/postgres/drop-db.sql')
            print("Database dropped successfully.")
        except Exception as e:
            print(f"Error during database drop: {e}")
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

def affinity_score_central_user():
    from model.user import User
    database = Database()
    central_user_id = User.get_central_user_id()
    all_users_data = database.getUsers()
    all_users = [User(user_id=data[0], email=data[1], first_name=data[3], last_name=data[4]) for data in all_users_data]

    for user in all_users:
        affinity_score = user.get_affinity_score_with_central_user(central_user_id)
        relationship_status = "buddies" if affinity_score == 100 else "friends" if affinity_score == 50 else "not friends"
        print(f"{user.first_name}'s relationship status with Central User is {relationship_status} with an affinity score of {affinity_score}.")

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
    
    def determine_affinity(self, relationship):
        """Determine the affinity score based on the relationship."""
        affinity_scores = {
            "not friends": 0,
            "friends": 50,
            "buddies": 100
        }
        return affinity_scores.get(relationship, None)

    def set_user_affinity(self, user_id, related_user_id, relationship):
        """Insert or update the affinity score between two users."""
        affinity_score = self.determine_affinity(relationship)
        if affinity_score is not None:
            query = """
            INSERT INTO user_affinities (user_id, related_user_id, affinity_score)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, related_user_id) DO UPDATE SET affinity_score = EXCLUDED.affinity_score;
            """
            execute_query(query, (user_id, related_user_id, affinity_score))
        else:
            print("Invalid relationship type provided.")
        
    # Inside the Database class in db.py

    def get_user_id_by_email(self, email):
        query = "SELECT id FROM users WHERE email = %s;"
        result = execute_query(query, (email,))
        return result[0][0] if result else None

    def getGroups(self):
        pass
    
    def getGroupMembers(self):
        pass


