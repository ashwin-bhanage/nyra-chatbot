"""
ChatLog Model - Stores all chat conversations
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ChatLog(Base):
    """
    ChatLog table - stores all chat messages
    Used for:
    - Conversation history
    - Analytics
    - Training AI
    - Debugging

    Relationships:
    - user: The customer who sent the message
    """

    __tablename__ = "chat_logs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # Session tracking (to group related messages)
    session_id = Column(String(100), nullable=False, index=True)

    # Message content
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)

    # Intent detected by AI (e.g., "menu_query", "place_order", "make_reservation")
    intent = Column(String(50), nullable=True, index=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="chat_logs")

    def __repr__(self):
        """String representation for debugging"""
        return f"<ChatLog(id={self.id}, user_id={self.user_id}, intent='{self.intent}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "intent": self.intent,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
