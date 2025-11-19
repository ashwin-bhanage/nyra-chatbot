"""
Order Router - API endpoints for order management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdateStatus, OrderListResponse
from app.services.order_service import order_service

router = APIRouter()


@router.post("/order", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order

    - **items**: List of menu items with quantities
    - **phone_number**: Customer phone (if not registered)
    - **delivery_address**: Delivery address (optional)
    - **special_instructions**: Special requests (optional)

    Returns created order with order ID
    """

    try:
        order = order_service.create_order(db, order_data)
        return order_service.format_order_response(order, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")


@router.get("/order/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get order details by ID

    - **order_id**: Order ID

    Returns order with all items and status
    """

    order = order_service.get_order(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    return order_service.format_order_response(order, db)


@router.get("/orders/user/{user_id}", response_model=OrderListResponse)
async def get_user_orders(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all orders for a user

    - **user_id**: User ID
    - **limit**: Maximum number of orders to return (default: 10)

    Returns list of orders
    """

    orders = order_service.get_user_orders(db, user_id, limit)

    order_responses = [
        order_service.format_order_response(order, db)
        for order in orders
    ]

    return OrderListResponse(
        orders=order_responses,
        total=len(order_responses)
    )


@router.put("/order/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderUpdateStatus,
    db: Session = Depends(get_db)
):
    """
    Update order status

    - **order_id**: Order ID
    - **status**: New status (pending, confirmed, preparing, ready, delivered, cancelled)

    Returns updated order
    """

    try:
        order = order_service.update_order_status(db, order_id, status_data.status)
        return order_service.format_order_response(order, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating order: {str(e)}")


@router.get("/order/{order_id}/summary")
async def get_order_summary(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get human-readable order summary

    - **order_id**: Order ID

    Returns formatted order summary text
    """

    order = order_service.get_order(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    summary = order_service.generate_order_summary(order, db)

    return {
        "order_id": order_id,
        "summary": summary
    }
