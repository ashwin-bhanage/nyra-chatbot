"""
Database Configuration - Supports MySQL (dev) and PostgreSQL (prod)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

DATABASE_URL = settings.database_url

if settings.is_production:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import menu, user, order, reservation, chat_log
    Base.metadata.create_all(bind=engine)
    print('Database tables created!')
