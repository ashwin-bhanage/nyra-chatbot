"""
Database initialization script
Run this once to create all tables
"""

from app.database import init_db, engine
from app.models import User, MenuItem, Order, OrderItem, Reservation, ChatLog

def main():
    """Create all database tables"""
    print("=" * 50)
    print("DATABASE INITIALIZATION")
    print("=" * 50)

    try:
        # Test connection first
        print("\n1. Testing database connection...")
        connection = engine.connect()
        print("✅ Connection successful!")
        connection.close()

        # Create tables
        print("\n2. Creating tables...")
        init_db()

        print("\n" + "=" * 50)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 50)
        print("\nTables created:")
        print("  - users")
        print("  - menu_items")
        print("  - orders")
        print("  - order_items")
        print("  - reservations")
        print("  - chat_logs")
        print("\nYou can now run the application!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if MySQL is running")
        print("2. Verify .env file has correct credentials")
        print("3. Ensure database 'restaurant_db' exists")
        print("   Run: CREATE DATABASE restaurant_db;")

if __name__ == "__main__":
    main()
