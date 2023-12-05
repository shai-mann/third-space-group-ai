from db import initialize_database, Database, affinity_score_central_user, drop_database

def main():
    # Drop database if needed. This is useful for testing.
    # drop_database()
    # Initialize database
    initialize_database()
    # Get affinity score for Central
    affinity_score_central_user()


if __name__ == "__main__":
    main()
