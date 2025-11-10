"""
User Model - Represents customers using the chatbot
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User table - stores customer information

    Relationships:
    - orders: All orders placed by this user
    - reservations: All reservations made by this user
    - chat_logs: All chat messages from this user
    """

    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # User details
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (one user can have many orders/reservations/chats)
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        """String representation for debugging"""
        return f"<User(id={self.id}, name='{self.name}', phone='{self.phone_number}')>"
