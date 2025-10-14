#!/usr/bin/env python3
"""
Simple Web Application Runner
This is a simplified version of run_web_app.py
"""

import subprocess
import sys
import webbrowser
import time
import threading

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

def main():
    print("🌐 Starting Disaster Relief Management System...")
    print("📱 Opening browser in 3 seconds...")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the Flask app
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")

if __name__ == "__main__":
    main()
