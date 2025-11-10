"""
Pydantic schemas for Menu operations
These define the structure of data going in/out of API
"""

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class MenuItemBase(BaseModel):
    """
    Base schema with common fields
    Used as parent for other schemas
    """
    name: str = Field(..., min_length=1, max_length=100, description="Name of the menu item")
    description: Optional[str] = Field(None, description="Description of the item")
    category: str = Field(..., description="Category: appetizer, main, dessert, or beverage")
    price: Decimal = Field(..., gt=0, description="Price must be greater than 0")
    is_available: bool = Field(True, description="Is item available for order?")
    image_url: Optional[str] = Field(None, max_length=255, description="URL to item image")


class MenuItemCreate(MenuItemBase):
    """
    Schema for creating a new menu item
    Used in POST requests
    """
    pass  # Inherits all fields from MenuItemBase


class MenuItemUpdate(BaseModel):
    """
    Schema for updating a menu item
    All fields are optional (can update just one field)
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    is_available: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=255)


class MenuItemResponse(MenuItemBase):
    """
    Schema for API responses
    Includes database-generated fields like id
    """
    id: int
    created_at: str

    class Config:
        # Allow conversion from SQLAlchemy model to Pydantic model
        from_attributes = True

        # Example of how this will look in API response
        json_schema_extra = {
            "example": {
                "id": 4,
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato, mozzarella, and basil",
                "category": "main",
                "price": 12.99,
                "is_available": True,
                "image_url": None,
                "created_at": "2025-11-09T03:09:23"
            }
        }


class MenuItemList(BaseModel):
    """
    Schema for returning list of menu items
    """
    items: list[MenuItemResponse]
    total: int
    category: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 4,
                        "name": "Margherita Pizza",
                        "description": "Classic pizza",
                        "category": "main",
                        "price": 12.99,
                        "is_available": True,
                        "image_url": None,
                        "created_at": "2025-11-09T03:09:23"
                    }
                ],
                "total": 1,
                "category": "main"
            }
        }
