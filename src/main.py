from db import initialize_database
from db_utils import drop_database


def main():
    # Drop database if needed. This is useful for testing.
    # drop_database()
    # Initialize database
    initialize_database()



if __name__ == "__main__":
    main()
