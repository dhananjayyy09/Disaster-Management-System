"""
Quick Demo Runner for Disaster Relief Management System
This script provides a simple way to run the demo and start the application
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'mysql-connector-python',
        'matplotlib',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def setup_database():
    """Setup the database"""
    print("🔧 Setting up database...")
    try:
        result = subprocess.run([sys.executable, "setup_database.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database setup completed successfully!")
            return True
        else:
            print("❌ Database setup failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def run_demo_scenarios():
    """Run demo scenarios to populate data"""
    print("🎭 Running demo scenarios...")
    try:
        result = subprocess.run([sys.executable, "demo_scenarios.py"], 
                              input="1\n", text=True, capture_output=True)
        if result.returncode == 0:
            print("✅ Demo scenarios completed successfully!")
            return True
        else:
            print("❌ Demo scenarios failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running demo scenarios: {e}")
        return False

def start_application():
    """Start the main application"""
    print("🚀 Starting Disaster Relief Management System...")
    try:
        subprocess.run([sys.executable, "main_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main demo runner"""
    print("🏥 Disaster Relief Management System - Demo Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    required_files = [
        "database_schema.sql",
        "main_app.py",
        "setup_database.py",
        "demo_scenarios.py"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease run this script from the project root directory.")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Setup database
    if not setup_database():
        print("\n⚠️  Database setup failed. Please check your MySQL installation.")
        print("You can still try to run the application manually:")
        print("python main_app.py")
        return
    
    # Ask user if they want to run demo scenarios
    print("\n" + "="*50)
    choice = input("Do you want to run demo scenarios to populate sample data? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        if not run_demo_scenarios():
            print("\n⚠️  Demo scenarios failed, but you can still run the application.")
    
    # Start the application
    print("\n" + "="*50)
    print("Starting the main application...")
    start_application()

if __name__ == "__main__":
    main()
