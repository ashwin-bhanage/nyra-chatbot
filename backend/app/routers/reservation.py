"""
Reservation Router - API endpoints for reservation management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationListResponse
from app.services.reservation_service import reservation_service

router = APIRouter()


@router.post("/reservation", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new table reservation

    - **reservation_date**: Date (YYYY-MM-DD)
    - **reservation_time**: Time (HH:MM)
    - **party_size**: Number of people (1-20)
    - **phone_number**: Customer phone (if not registered)
    - **special_requests**: Special requests (optional)

    Returns created reservation with reservation ID
    """

    try:
        reservation = reservation_service.create_reservation(db, reservation_data)
        return reservation_service.format_reservation_response(reservation)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating reservation: {str(e)}")


@router.get("/reservation/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get reservation details by ID

    - **reservation_id**: Reservation ID

    Returns reservation details
    """

    reservation = reservation_service.get_reservation(db, reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail=f"Reservation {reservation_id} not found")

    return reservation_service.format_reservation_response(reservation)


@router.get("/reservations/user/{user_id}", response_model=ReservationListResponse)
async def get_user_reservations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all reservations for a user

    - **user_id**: User ID
    - **limit**: Maximum number to return (default: 10)

    Returns list of reservations
    """

    reservations = reservation_service.get_user_reservations(db, user_id, limit)

    reservation_responses = [
        reservation_service.format_reservation_response(res)
        for res in reservations
    ]

    return ReservationListResponse(
        reservations=reservation_responses,
        total=len(reservation_responses)
    )


@router.put("/reservation/{reservation_id}/status")
async def update_reservation_status(
    reservation_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Update reservation status

    - **reservation_id**: Reservation ID
    - **status**: New status (pending, confirmed, cancelled)

    Returns updated reservation
    """

    try:
        reservation = reservation_service.update_reservation_status(db, reservation_id, status)
        return reservation_service.format_reservation_response(reservation)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating reservation: {str(e)}")


@router.delete("/reservation/{reservation_id}")
async def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancel a reservation

    - **reservation_id**: Reservation ID

    Returns cancelled reservation
    """

    try:
        reservation = reservation_service.cancel_reservation(db, reservation_id)
        return {
            "message": "Reservation cancelled successfully",
            "reservation": reservation_service.format_reservation_response(reservation)
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling reservation: {str(e)}")


@router.get("/reservation/{reservation_id}/summary")
async def get_reservation_summary(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get human-readable reservation summary

    - **reservation_id**: Reservation ID

    Returns formatted reservation summary text
    """

    reservation = reservation_service.get_reservation(db, reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail=f"Reservation {reservation_id} not found")

    summary = reservation_service.generate_reservation_summary(reservation)

    return {
        "reservation_id": reservation_id,
        "summary": summary
    }
