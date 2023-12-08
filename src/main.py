from db import initialize_database, assign_affinities
from db_utils import drop_database

def main():
    # Drop database if needed. This is useful for testing.
    drop_database()
    # Initialize database
    initialize_database()

    # for data set construction only:
    assign_affinities()

if __name__ == "__main__":
    main()
