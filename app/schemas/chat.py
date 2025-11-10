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

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me your pizzas",
                "user_id": 1,
                "session_id": "session_abc123",
                "phone_number": "+1234567890"
            }
        }


class ChatResponse(BaseModel):
    """
    Schema for chatbot responses
    """
    response: str = Field(..., description="Bot's response message")
    intent: Optional[str] = Field(None, description="Detected intent (menu_query, order, etc.)")
    session_id: str
    data: Optional[dict] = Field(None, description="Additional data (menu items, order details, etc.)")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Here are our delicious pizzas: Margherita ($12.99), Pepperoni ($14.99)",
                "intent": "menu_query",
                "session_id": "session_abc123",
                "data": {
                    "items": [
                        {"id": 4, "name": "Margherita Pizza", "price": 12.99},
                        {"id": 5, "name": "Pepperoni Pizza", "price": 14.99}
                    ]
                }
            }
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
