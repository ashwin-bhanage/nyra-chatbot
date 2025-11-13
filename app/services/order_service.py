"""
Order Service - Business logic for order management
"""

from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User
from app.models.menu import MenuItem
from app.schemas.order import OrderCreate, OrderItemResponse, OrderResponse
from typing import List, Optional
from decimal import Decimal


class OrderService:
    """Service for managing orders"""

    def create_order(
        self,
        db: Session,
        order_data: OrderCreate
    ) -> Order:
        """
        Create new order

        Args:
            db: Database session
            order_data: Order creation data

        Returns:
            Created order
        """
        #Get or create user
        if order_data.user_id:
            # ⭐ CHANGED — auto-create if user_id invalid
            user = db.query(User).filter(User.id == order_data.user_id).first()
            if not user:
                user = User(
                    id=order_data.user_id,      # ⭐ ADDED: Preserve ID if passed
                    phone_number=order_data.phone_number,
                    name="Guest User"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            user_id = user.id
        elif order_data.phone_number:
            # ⭐ CHANGED — get or create user properly
            user = db.query(User).filter(User.phone_number == order_data.phone_number).first()

            if not user:
                user = User(
                    phone_number=order_data.phone_number,
                    name="Guest User",   # ⭐ ADDED
                    email=None           # ⭐ ADDED
                )
                db.add(user)
                db.commit()             # ⭐ IMPORTANT FIX
                db.refresh(user)

            user_id = user.id
        else:
            raise ValueError("Either user_id or phone_number is required")

        # Calculate total and create order items
        total_amount = Decimal('0.00')
        order_items_data = []

        for item_data in order_data.items:
            # Get menu item
            menu_item = db.query(MenuItem).filter(
                MenuItem.id == item_data.menu_item_id,
                MenuItem.is_available == True
            ).first()

            if not menu_item:
                raise ValueError(f"Menu item {item_data.menu_item_id} not available")

            # Calculate subtotal
            subtotal = menu_item.price * item_data.quantity
            total_amount += subtotal

            order_items_data.append({
                'menu_item_id': menu_item.id,
                'menu_item': menu_item,
                'quantity': item_data.quantity,
                'price_at_order': menu_item.price
            })

        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            delivery_address=order_data.delivery_address,
            special_instructions=order_data.special_instructions
        )

        db.add(order)
        db.flush()

        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item_data['menu_item_id'],
                quantity=item_data['quantity'],
                price_at_order=item_data['price_at_order']
            )
            db.add(order_item)

        db.commit()
        db.refresh(order)

        return order

    def get_order(
        self,
        db: Session,
        order_id: int
    ) -> Optional[Order]:
        """Get order by ID"""
        return db.query(Order).filter(Order.id == order_id).first()

    def get_user_orders(
        self,
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[Order]:
        """Get orders for a user"""
        return db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(
            Order.created_at.desc()
        ).limit(limit).all()

    def update_order_status(
        self,
        db: Session,
        order_id: int,
        new_status: str
    ) -> Order:
        """Update order status"""
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise ValueError(f"Order {order_id} not found")

        # Validate status
        try:
            status_enum = OrderStatus(new_status.lower())
        except ValueError:
            raise ValueError(f"Invalid status: {new_status}")

        order.status = status_enum
        db.commit()
        db.refresh(order)

        return order

    def format_order_response(
        self,
        order: Order,
        db: Session
    ) -> OrderResponse:
        """Format order for API response"""

        # Get order items with menu item details
        items = []
        for order_item in order.items:
            menu_item = db.query(MenuItem).filter(
                MenuItem.id == order_item.menu_item_id
            ).first()

            items.append(OrderItemResponse(
                id=order_item.id,
                menu_item_id=order_item.menu_item_id,
                menu_item_name=menu_item.name if menu_item else "Unknown Item",
                quantity=order_item.quantity,
                price_at_order=order_item.price_at_order,
                subtotal=order_item.price_at_order * order_item.quantity
            ))

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            status=order.status.value,
            total_amount=order.total_amount,
            delivery_address=order.delivery_address,
            special_instructions=order.special_instructions,
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat() if order.updated_at else order.created_at.isoformat(),
            items=items
        )

    def generate_order_summary(
        self,
        order: Order,
        db: Session
    ) -> str:
        """Generate human-readable order summary"""

        lines = [
            f"🧾 **Order #{order.id}**",
            f"Status: {order.status.value.upper()}",
            f"",
            "**Items:**"
        ]

        for order_item in order.items:
            menu_item = db.query(MenuItem).filter(
                MenuItem.id == order_item.menu_item_id
            ).first()

            subtotal = order_item.price_at_order * order_item.quantity
            lines.append(
                f"- {order_item.quantity}x {menu_item.name if menu_item else 'Item'} "
                f"(${order_item.price_at_order} each) = ${subtotal}"
            )

        lines.extend([
            "",
            f"**Total: ${order.total_amount}**",
            "",
            f"📍 Delivery: {order.delivery_address if order.delivery_address else 'Pickup'}",
        ])

        if order.special_instructions:
            lines.append(f"📝 Note: {order.special_instructions}")

        return "\n".join(lines)


# Create singleton instance
order_service = OrderService()
