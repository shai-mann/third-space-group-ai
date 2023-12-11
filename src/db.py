"""
This is where database interface code goes
"""

from db_connection import execute_query, connect_db, execute_sql_file
from db_utils import should_update_schema
import random


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
            users_id = database.getUsersIds()

            print("Database initialized successfully.")

            central_user_id = 0  # Set this to the ID of your central user

            for user_id_tuple in users_id:
                user_id = user_id_tuple[0]
                user_info = database.get_user_features(user_id, central_user_id)
                print(f"Info for user {user_id} based on central user: {user_info}")


        except Exception as e:
            print(f"Error initializing the database: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


def assign_affinities():
    conn = connect_db()
    if conn:
        db = Database()
        open("src/postgres/affinities.sql", "w").close()
        file = open("src/postgres/affinities.sql", "a")
        file.write("INSERT INTO affinities (\"user\", user_other, affinity_score) VALUES\n")
        ids = db.getUsersIds()
        size = len(ids)
        for (index, (id)) in enumerate(ids):
            if (id == 0):
                continue
            [features] = db.get_user_features(id, 0)
            # (age difference, are buddies, are friends, # friends in common, # hobbies in common, # groups in common)
            print(
                f"""User {id}
Age difference: {features[0]}
Buddy? {"YES" if features[1] == 1 else "NO"}
Friends? {"YES" if features[2] == 1 else "NO"}
Number of Shared Friends: {features[3]}
Number of Shared Hobbies: {features[4]}
Number of Shared Groups: {features[5]}
"""
            )
            # Automatically determine the affinity score
            if features[1] == 1:  # Buddies
                affinity = 100
            elif features[2] == 1:  # Friends but not buddies
                affinity = 50
            else:  # Neither buddies nor friends
                affinity = 0
            ending_char = "," if index < size else ";"
            file.write(f"({0}, {id[0]}, {affinity}){ending_char}\n")
            print("================================")

        print("Affinities assigned successfully")
    else:
        print("Failed to assign affinities.")
        file.close()
    
def random_affinities():
    conn = connect_db()
    if conn:
        db = Database()
        with open("src/postgres/random_affinities.sql", "w") as file:
            file.write("INSERT INTO affinities (\"user\", user_other, affinity_score) VALUES\n")
            ids = db.getUsersIds()
            for (index, (id,)) in enumerate(ids):
                if id == 0:
                    continue
                # Assign a random affinity score
                affinity = random.choice([0, 50, 100])
                ending_char = "," if index < len(ids) - 1 else ";"
                file.write(f"({0}, {id}, {affinity}){ending_char}\n")
                print(f"User {id}: Randomly assigned affinity score {affinity}")
                print("================================")

            print("Random affinities written to SQL file.")
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
    
    def get_user_features(self, user_id, central_user_id):
        query = "SELECT * FROM get_user_features(%s, %s);"
        return execute_query(query, (user_id, central_user_id))


    




