"""
Database Setup Script for Disaster Relief Management System
This script sets up the database and populates it with sample data.
"""

import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DJdjdj12'  
}
DB_NAME = 'disaster_relief_db'
SCHEMA_FILE = 'database_schema.sql'

def create_database():
    """Create the database and tables from the schema file."""
    connection = None  # Initialize connection to None
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()
            print("Successfully connected to MySQL server.")

            # Check if database exists
            cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print(f"Database '{DB_NAME}' already exists.")
                choice = input("Do you want to recreate it? This will delete all existing data! (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    cursor.execute(f"DROP DATABASE {DB_NAME}")
                    print(f"Database '{DB_NAME}' dropped.")
                else:
                    print("Using existing database.")
                    return True

            # Read and execute the SQL schema file
            print(f"Reading schema from '{SCHEMA_FILE}'...")
            with open(SCHEMA_FILE, 'r') as file:
                # Split script into individual statements, ignoring empty ones
                sql_script = file.read()
                statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

            print(f"Found {len(statements)} SQL statements to execute.")
            for statement in statements:
                try:
                    cursor.execute(statement)
                except Error as e:
                    # Check if it's a "table already exists" error
                    if e.errno == 1050:  # Table already exists
                        print(f"⚠️  Table already exists, skipping: {statement[:50]}...")
                        continue
                    else:
                        # Provide more context on which statement failed
                        print(f"\n--- Error executing statement ---\n{statement}\nError: {e}\n")
                        return False # Stop execution on first error

            connection.commit()
            print("\n✅ Database schema and data loaded successfully!")
            return True

    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False
    finally:
        # Only try to close if the connection was successfully established
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def check_database_connection():
    """Check if the database and tables were created correctly."""
    connection = None # Initialize connection to None
    try:
        # Connect directly to the newly created database
        connection = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)

        if connection.is_connected():
            print("\nDatabase connection test successful!")
            cursor = connection.cursor()

            # Check counts in major tables
            tables_to_check = ["disasters", "relief_camps", "volunteers", "donations"]
            print("Verifying sample data counts:")
            for table in tables_to_check:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  - Found {count} records in '{table}'")
            return True

    except Error as e:
        print(f"❌ Error connecting to the '{DB_NAME}' database: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main setup function."""
    print("Disaster Relief Management System - Database Setup")
    print("=" * 50)

    # 1. Check if the schema file exists
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ Error: '{SCHEMA_FILE}' not found in the current directory!")
        return

    # 2. Create the database and tables
    print("Step 1: Setting up database...")
    if not create_database():
        print("\nDatabase setup failed. Please check the errors above.")
        return

    # 3. Test the connection and verify data
    print("\nStep 2: Testing database connection...")
    if check_database_connection():
        print("\n🎉 All done! Your database is ready.")
        print("You can now run the main application.")
    else:
        print("\nDatabase connection test failed.")

if __name__ == "__main__":
    main()