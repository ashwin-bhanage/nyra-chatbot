"""
Order Models - Represents customer orders and order items
"""

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """Possible order statuses"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    """
    Order table - stores customer orders

    Relationships:
    - user: The customer who placed the order
    - items: All items in this order (OrderItem)
    """

    __tablename__ = "orders"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Order details
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )

    # Delivery information
    delivery_address = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        """String representation for debugging"""
        return f"<Order(id={self.id}, user_id={self.user_id}, total=${self.total_amount}, status='{self.status}')>"


class OrderItem(Base):
    """
    OrderItem table - links orders with menu items
    (Many-to-many relationship between Order and MenuItem)
    """

    __tablename__ = "order_items"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign keys
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False, index=True)

    # Item details at time of order
    quantity = Column(Integer, nullable=False, default=1)
    price_at_order = Column(Numeric(10, 2), nullable=False)  # Price when ordered (in case menu price changes)

    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    def __repr__(self):
        """String representation for debugging"""
        return f"<OrderItem(order_id={self.order_id}, menu_item_id={self.menu_item_id}, qty={self.quantity})>"
