"""
Pydantic schemas for Order operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schema for creating order item"""
    menu_item_id: int = Field(..., description="Menu item ID")
    quantity: int = Field(..., gt=0, description="Quantity (must be > 0)")


class OrderItemResponse(BaseModel):
    """Schema for order item in response"""
    id: int
    menu_item_id: int
    menu_item_name: str
    quantity: int
    price_at_order: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating new order"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = Field(None, description="Phone number if user not registered")
    items: List[OrderItemCreate] = Field(..., min_length=1, description="At least one item required")
    delivery_address: Optional[str] = Field(None, max_length=500)
    special_instructions: Optional[str] = Field(None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+1234567890",
                "items": [
                    {"menu_item_id": 4, "quantity": 2},
                    {"menu_item_id": 12, "quantity": 1}
                ],
                "delivery_address": "123 Main St, Apt 4B",
                "special_instructions": "Extra napkins please"
            }
        }


class OrderResponse(BaseModel):
    """Schema for order in response"""
    id: int
    user_id: Optional[int]
    status: str
    total_amount: Decimal
    delivery_address: Optional[str]
    special_instructions: Optional[str]
    created_at: str
    updated_at: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "status": "pending",
                "total_amount": 28.97,
                "delivery_address": "123 Main St",
                "special_instructions": "Ring doorbell",
                "created_at": "2025-11-09T15:30:00",
                "updated_at": "2025-11-09T15:30:00",
                "items": [
                    {
                        "id": 1,
                        "menu_item_id": 4,
                        "menu_item_name": "Margherita Pizza",
                        "quantity": 2,
                        "price_at_order": 12.99,
                        "subtotal": 25.98
                    }
                ]
            }
        }


class OrderUpdateStatus(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., description="Order status: pending, confirmed, preparing, ready, delivered, cancelled")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "confirmed"
            }
        }


class OrderListResponse(BaseModel):
    """Schema for list of orders"""
    orders: List[OrderResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "orders": [],
                "total": 0
            }
        }
