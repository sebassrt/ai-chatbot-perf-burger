#!/usr/bin/env python3
"""
Database initialization script for PerfBurger Chatbot
Run this script to create all necessary database tables.
"""

from app import create_app, db
from app.models import User, Order, ChatSession, ChatMessage

def init_database():
    """Initialize the database with all required tables"""
    print("🔧 Initializing PerfBurger Chatbot Database...")
    
    # Create Flask application
    app = create_app()
    
    # Push application context
    with app.app_context():
        try:
            # Create all database tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print created tables info
            print("\n📋 Created tables:")
            print("   - users (for authentication)")
            print("   - orders (for order tracking)")
            print("   - chat_sessions (for conversation management)")
            print("   - chat_messages (for individual messages)")
            
            print(f"\n💾 Database file: chatbot.db")
            print("🚀 Your chatbot is ready to run!")
            
        except Exception as e:
            print(f"❌ Error creating database: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database initialization completed successfully!")
        print("You can now run: python run.py")
    else:
        print("\n💥 Database initialization failed!")
        exit(1)
