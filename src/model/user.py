"""
Stores the model information for Users.
"""
import sys
sys.path.insert(0, 'src')
from db import Database, execute_query

class User:
    """
    This file stores information about the User model in the database. It
    stores any useful or relevant data to a given User in the Users table.
    """

    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.database = Database()
        self.affinity_score = self.get_affinity_score()
        self.relationship_status = self.get_relationship_status()

    def get_affinity_score(self):
        """
        Retrieve the affinity score for the user from the database.
        """
        # Implement the logic to retrieve the affinity score for this user from the database.
        # You will need to modify this to match your database schema and tables.
        query = """
        SELECT affinity_score FROM user_affinities
        WHERE user_id = %s;
        """
        result = execute_query(query, (self.user_id,))
        return result[0][0] if result else 0  # Default to 0 if no data is found

    def get_relationship_status(self):
        """
        Determine the relationship status based on the affinity score.
        """
        if self.affinity_score == 100:
            return "buddies"
        elif self.affinity_score == 50:
            return "friends"
        else:
            return "not friends"
        
    def get_affinity_score_with_karim(self, karim_user_id):
        """
        Retrieve the affinity score for the user in relation to Karim from the database.
        """
        query = """
        SELECT affinity_score FROM user_affinities
        WHERE user_id = %s AND related_user_id = %s;
        """
        result = execute_query(query, (karim_user_id, self.user_id))
        # Assuming a bidirectional relationship, you might also want to check the inverse
        if not result:
            result = execute_query(query, (self.user_id, karim_user_id))
        return result[0][0] if result else 0  # Default to 0 if no data is found
    
    @classmethod
    def get_karims_id(cls):
        """
        Get Karim's user ID from the database using his known unique email.
        """
        database = Database()
        return database.get_user_id_by_email('karim.semaan@example.com')


# You would instantiate User objects after retrieving user data from the database
# Assuming you have Karim's user ID
karim_user_id = User.get_karims_id()
all_users_data = Database().getUsers()
all_users = [User(user_id=data[0], email=data[1], first_name=data[3], last_name=data[4]) for data in all_users_data]

for user in all_users:
    affinity_score = user.get_affinity_score_with_karim(karim_user_id)
    relationship_status = "buddies" if affinity_score == 100 else "friends" if affinity_score == 50 else "not friends"
    print(f"{user.first_name}'s relationship status with Karim is {relationship_status} with an affinity score of {affinity_score}.")
