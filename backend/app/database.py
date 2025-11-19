"""
Database connection and session management
This file sets up SQLAlchemy to connect to MySQL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
# echo=True means it will print all SQL queries (good for learning/debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Print SQL queries in debug mode
    pool_pre_ping=True,   # Check connection before using it
    pool_recycle=3600     # Recycle connections every hour
)

# Session factory - creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit changes
    autoflush=False,   # Don't auto-flush changes
    bind=engine        # Bind to our engine
)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    This will be used in FastAPI endpoints

    Usage in endpoint:
    @app.get("/example")
    def example(db: Session = Depends(get_db)):
        # use db here
    """
    db = SessionLocal()
    try:
        yield db  # Provide database session
    finally:
        db.close()  # Always close connection when done


def init_db():
    """
    Initialize database - create all tables
    Call this once when starting the app
    """
    from app.models import user, menu, order, reservation, chat_log

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_all_tables():
    """
    Drop all tables - USE WITH CAUTION!
    Only use for development/testing
    """
    print("⚠️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped!")


# Test connection
if __name__ == "__main__":
    try:
        # Try to connect
        connection = engine.connect()
        print("✅ Database connection successful!")
        print(f"Connected to: {settings.DB_NAME}")
        connection.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Is MySQL running?")
        print("2. Is the password in .env correct?")
        print("3. Does the database exist? Create it with:")
        print(f"   CREATE DATABASE {settings.DB_NAME};")
