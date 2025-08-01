#!/usr/bin/env python3
"""Debug script to check database configuration and connection"""

import os
import sqlite3
from config import Config

def check_database():
    print("🔍 Database Debug Information")
    print("=" * 50)
    
    # Check environment variables
    print("Environment Variables:")
    print(f"WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME', 'Not set')}")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    
    # Check config
    config = Config()
    print(f"\nConfig Database URI: {config.SQLALCHEMY_DATABASE_URI}")
    
    # Extract database path from SQLite URI
    if config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
        db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        print(f"Database file path: {db_path}")
        print(f"Absolute path: {os.path.abspath(db_path)}")
        print(f"File exists: {os.path.exists(db_path)}")
        print(f"File readable: {os.access(db_path, os.R_OK) if os.path.exists(db_path) else 'N/A'}")
        print(f"File writable: {os.access(db_path, os.W_OK) if os.path.exists(db_path) else 'N/A'}")
        
        # Try direct SQLite connection
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables in database: {[table[0] for table in tables]}")
            conn.close()
            print("✅ Direct SQLite connection successful!")
        except Exception as e:
            print(f"❌ Direct SQLite connection failed: {e}")
    
    # Check directory permissions
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, 'instance')
    print(f"\nInstance directory: {instance_dir}")
    print(f"Instance dir exists: {os.path.exists(instance_dir)}")
    print(f"Instance dir readable: {os.access(instance_dir, os.R_OK) if os.path.exists(instance_dir) else 'N/A'}")
    print(f"Instance dir writable: {os.access(instance_dir, os.W_OK) if os.path.exists(instance_dir) else 'N/A'}")

if __name__ == "__main__":
    check_database()
