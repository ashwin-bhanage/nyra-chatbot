"""
Pydantic schemas for Chat operations
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    Schema for incoming chat messages
    """
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    user_id: Optional[int] = Field(None, description="User ID (if registered)")
    session_id: str = Field(..., description="Session ID to track conversation")
    phone_number: Optional[str] = Field(None, max_length=15, description="User's phone number")
    email: Optional[str] = None      # ⭐ ADDED

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me your pizzas",
                "user_id": 1,
                "session_id": "session_abc123",
                "phone_number": "+1234567890",
                "email": "john@example.com"

            }
        }


class ChatResponse(BaseModel):
    """
    Schema for chatbot responses
    """
    response: str = Field(..., description="Bot's response message")
    intent: Optional[str] = Field(None, description="Detected intent (menu_query, order, etc.)")
    session_id: str
    user_id: Optional[int] = None
    data: Optional[dict] = Field(None, description="Additional data (menu items, order details, etc.)")
    action: Optional[str] = Field(None, description="Action taken (order_created, reservation_created, etc.)")
    order_id: Optional[int] = None
    reservation_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Great! Your order has been placed successfully!",
                "intent": "order_intent",
                "session_id": "session_abc123",
                "user_id": 1,
                "data": {},
                "action": "order_created",
                "order_id": 1
            },

        }


class ChatHistoryResponse(BaseModel):
    """
    Schema for chat history
    """
    id: int
    user_message: str
    bot_response: str
    intent: Optional[str]
    timestamp: str

    class Config:
        from_attributes = True
