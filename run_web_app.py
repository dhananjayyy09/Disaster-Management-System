"""
Web Application Runner for Disaster Relief Management System
This script provides a simple way to run the web application
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'mysql-connector-python',
        'matplotlib',
        'pandas',
        'numpy'
    ]
    
    return True

def check_database():
    """Check if database is set up"""
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager()
        if db.connect():
            print("✅ Database connection successful!")
            db.disconnect()
            return True
        else:
            print("❌ Database connection failed!")
            print("Please run: python setup_database.py")
            return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def run_web_application():
    """Run the Flask web application"""
    print("🌐 Starting Disaster Relief Management System Web Application...")
    print("📱 The application will open in your default browser")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run Flask app
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Web application stopped by user")

def main():
    """Main function"""
    print("🏥 Disaster Relief Management System - Web Application")
    print("=" * 50)
    
    # Check if we're in the right directory
    required_files = [
        "app.py",
        "database_manager.py",
        "templates",
        "static"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease run this script from the project root directory.")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check database
    if not check_database():
        print("\n⚠️  Database setup failed. You can still try to run the application manually:")
        print("python app.py")
        choice = input("\nDo you want to continue anyway? (y/n): ").lower().strip()
        if choice not in ['y', 'yes']:
            return
    
    # Run the web application
    run_web_application()

if __name__ == "__main__":
    main()
