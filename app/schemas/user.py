"""
Pydantic schemas for User operations
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    phone_number: str = Field(..., min_length=10, max_length=15, description="User's phone number")
    name: Optional[str] = Field(None, max_length=100, description="User's name")
    email: Optional[EmailStr] = Field(None, description="User's email")


class UserCreate(UserBase):
    """Schema for creating new user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user - all fields optional"""
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema for user in responses"""
    id: int
    created_at: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "phone_number": "+1234567890",
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2025-11-09T03:00:00"
            }
        }
