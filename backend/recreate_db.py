#!/usr/bin/env python3
"""
Force database schema recreation for PerfBurger Chatbot
This will drop and recreate all tables to apply schema changes.
"""

from app import create_app, db
from app.models import User, Order, ChatSession, ChatMessage

def recreate_database():
    """Drop and recreate all database tables"""
    print("🔧 Recreating PerfBurger Chatbot Database Schema...")
    
    # Create Flask application
    app = create_app()
    
    # Push application context
    with app.app_context():
        try:
            # Drop all existing tables
            print("🗑️ Dropping existing tables...")
            db.drop_all()
            
            # Create all database tables with new schema
            print("🔧 Creating tables with updated schema...")
            db.create_all()
            print("✅ Database schema recreated successfully!")
            
            # Print created tables info
            print("\n📋 Recreated tables:")
            print("   - users (for authentication)")
            print("   - orders (for order tracking) - delivery_address now nullable")
            print("   - chat_sessions (for conversation management)")
            print("   - chat_messages (for individual messages)")
            
            print(f"\n💾 Database file: chatbot.db")
            print("🚀 Your chatbot is ready to run!")
            
        except Exception as e:
            print(f"❌ Error recreating database: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = recreate_database()
    if success:
        print("\n🎉 Database schema recreation completed successfully!")
        print("You can now run: python run.py")
    else:
        print("\n💥 Database schema recreation failed!")
        exit(1)
