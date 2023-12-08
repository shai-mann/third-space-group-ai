"""
This is where database interface code goes
"""

from db_connection import execute_query, connect_db, execute_sql_file
from db_utils import should_update_schema


def initialize_database():
    conn = connect_db()
    if conn:
        try:
            schema_updated = False  

            if should_update_schema(conn):
                execute_sql_file(conn, 'src/postgres/schema.sql')
                print("Schema updated successfully.")
                schema_updated = True 
            else:
                print("No Schema update needed.")

            # Check if schema was updated successfully before running data.sql
            if schema_updated:

                # Execute data.sql
                execute_sql_file(conn, 'src/postgres/data.sql')
                print("Data updated successfully.")

                # Execute get_user_info.sql to create the function in the database
                execute_sql_file(conn, 'src/postgres/get_user_features.sql')
                print("get_user_info function created successfully.")
            else:
                print("Data and Function update skipped as schema was not updated.")

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
                user_info = database.get_user_features(user_id[0])
                print(f"Info for user {user_id[0]} based on central user: {user_info}")

        except Exception as e:
            print(f"Error initializing the database: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")



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
        
    def get_user_id_by_email(self, email):
        query = "SELECT id FROM users WHERE email = %s;"
        result = execute_query(query, (email,))
        return result[0][0] if result else None
    
    def get_user_features(self, user_id):
        query = "SELECT * FROM get_user_features(%s);"
        return execute_query(query, (user_id,))
    

    




