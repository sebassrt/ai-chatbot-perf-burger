#!/usr/bin/env python3
"""
Debug script to test database connection
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("🔍 Database Connection Debug")
print("=" * 40)

# Check environment variables
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
print(f"WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME', 'Not set')}")
print(f"Current working directory: {os.getcwd()}")

# Check if we're on Azure
if os.environ.get('WEBSITE_HOSTNAME'):
    db_path = os.path.join('/tmp', 'chatbot.db')
    print(f"Running on Azure, using path: {db_path}")
else:
    # Local development
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, 'instance')
    db_path = os.path.join(instance_dir, 'chatbot.db')
    print(f"Running locally, using path: {db_path}")
    
    # Check if instance directory exists
    print(f"Instance directory exists: {os.path.exists(instance_dir)}")
    print(f"Database file exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        print(f"Database file size: {file_size} bytes")
        
        # Test if file is readable
        try:
            with open(db_path, 'rb') as f:
                f.read(16)  # Read first 16 bytes
            print("✅ Database file is readable")
        except Exception as e:
            print(f"❌ Cannot read database file: {e}")

# Test database connection
print("\n🔌 Testing database connection...")
try:
    from app import create_app, db
    
    app = create_app()
    with app.app_context():
        # Try to connect to database
        db.engine.connect()
        print("✅ Database connection successful!")
        
        # List tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Tables in database: {tables}")
        
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    import traceback
    traceback.print_exc()
