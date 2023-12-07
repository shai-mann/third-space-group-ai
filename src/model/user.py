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
        from db import execute_query
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
        
    def get_affinity_score_with_central_user(self, central_user_id):
        """
        Retrieve the affinity score for the user in relation to central user from the database.
        """
        query = """
        SELECT affinity_score FROM user_affinities
        WHERE user_id = %s AND related_user_id = %s;
        """
        result = execute_query(query, (central_user_id, self.user_id))
        # Assuming a bidirectional relationship, you might also want to check the inverse
        if not result:
            result = execute_query(query, (self.user_id, central_user_id))
        return result[0][0] if result else 0  # Default to 0 if no data is found
    
    @classmethod
    def get_central_user_id(cls):
        """
        Get Central's user ID from the database using his known unique email.
        """
        database = Database()
        return database.get_user_id_by_email('karim.semaan@example.com')
    


