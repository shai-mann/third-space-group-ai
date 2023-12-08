from db_connection import connect_db, execute_sql_file, check_table_exists



def should_update_schema(conn):
    """
    Determine whether the schema needs to be updated by checking the existence of multiple tables.
    """
    tables_to_check = ['users', 'hobbies', 'user_hobbies', 'friends', 'groups', 'group_members', 'affinities']
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



