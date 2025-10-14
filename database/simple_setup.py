"""
Simple Database Setup for Disaster Relief Management System
This version tries different MySQL connection configurations
"""

import mysql.connector
from mysql.connector import Error
import os

def try_database_connection():
    """Try different MySQL connection configurations"""
    configs = [
        # No password
        {'host': 'localhost', 'user': 'root', 'password': ''},
        # Common default password
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'user': 'root', 'password': 'password'},
        {'host': 'localhost', 'user': 'root', 'password': 'admin'},
        # Try with different host
        {'host': '127.0.0.1', 'user': 'root', 'password': ''},
    ]
    
    for i, config in enumerate(configs):
        try:
            print(f"Trying configuration {i+1}: {config}")
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print(f"✅ Successfully connected with config {i+1}!")
                connection.close()
                return config
        except Error as e:
            print(f"❌ Failed: {e}")
            continue
    
    return None

def create_database_with_config(config):
    """Create database using the working configuration"""
    try:
        # Connect to MySQL server (without database)
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS disaster_relief_db")
            print("✅ Database 'disaster_relief_db' created successfully!")
            
            # Use the database
            cursor.execute("USE disaster_relief_db")
            
            # Read and execute the SQL schema file
            if os.path.exists('database_schema.sql'):
                with open('database_schema.sql', 'r') as file:
                    sql_script = file.read()
                
                # Split the script into individual statements
                statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement and not statement.startswith('CREATE DATABASE'):
                        try:
                            cursor.execute(statement)
                            print(f"✅ Executed: {statement[:50]}...")
                        except Error as e:
                            print(f"⚠️  Error executing statement: {e}")
                
                connection.commit()
                print("✅ Database setup completed successfully!")
                
                # Test the setup
                cursor.execute("SELECT COUNT(*) FROM disasters")
                disaster_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM relief_camps")
                camp_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM volunteers")
                volunteer_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM donations")
                donation_count = cursor.fetchone()[0]
                
                print(f"\n📊 Sample data loaded:")
                print(f"  - Disasters: {disaster_count}")
                print(f"  - Relief Camps: {camp_count}")
                print(f"  - Volunteers: {volunteer_count}")
                print(f"  - Donations: {donation_count}")
                
                return True
            else:
                print("❌ database_schema.sql file not found!")
                return False
            
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

def main():
    """Main setup function"""
    print("🏥 Disaster Relief Management System - Simple Database Setup")
    print("=" * 60)
    
    # Try to find working MySQL configuration
    config = try_database_connection()
    
    if config:
        print(f"\n🔧 Using configuration: {config}")
        
        # Create database with working config
        if create_database_with_config(config):
            print("\n🎉 Database setup completed successfully!")
            print("You can now run the web application with:")
            print("py -3.11 run_web_app.py")
        else:
            print("\n❌ Database setup failed!")
    else:
        print("\n❌ Could not connect to MySQL!")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. MySQL is installed correctly")
        print("3. Try setting a password for root user")
        print("\nTo set MySQL root password:")
        print("mysql -u root -p")
        print("ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';")

if __name__ == "__main__":
    main()
