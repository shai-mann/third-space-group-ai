from db import connect_db

def main():
    # Connect to the database
    conn = connect_db()
    if conn:
        print("Connected to the database successfully.")
        conn.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
