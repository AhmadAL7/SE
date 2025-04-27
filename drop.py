import os

DB_FILE = 'restaurant.db'

def drop_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Database {DB_FILE} deleted successfully.")
    else:
        print(f"Database {DB_FILE} does not exist.")

if __name__ == "__main__":
    drop_database()
