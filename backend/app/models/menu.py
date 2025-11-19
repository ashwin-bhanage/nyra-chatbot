"""
Menu Model - Represents restaurant menu items
"""

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MenuCategory(str, enum.Enum):
    """Available menu categories"""
    APPETIZER = "appetizer"
    MAIN = "main"
    DESSERT = "dessert"
    BEVERAGE = "beverage"


class MenuItem(Base):
    """
    MenuItem table - stores all menu items

    Relationships:
    - order_items: Links to orders that include this item
    """

    __tablename__ = "menu_items"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Item details
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(
        Enum(MenuCategory),
        nullable=False,
        index=True
    )

    # Pricing
    price = Column(Numeric(10, 2), nullable=False)  # e.g., 12.99

    # Availability
    is_available = Column(Boolean, default=True, nullable=False)

    # Optional image
    image_url = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order_items = relationship("OrderItem", back_populates="menu_item")

    def __repr__(self):
        """String representation for debugging"""
        return f"<MenuItem(id={self.id}, name='{self.name}', price=${self.price}, category='{self.category}')>"

    def to_dict(self):
        """Convert to dictionary for easy JSON conversion"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "price": float(self.price),
            "is_available": self.is_available,
            "image_url": self.image_url
        }
