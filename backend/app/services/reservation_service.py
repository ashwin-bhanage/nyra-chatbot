"""
Reservation Service - Business logic for reservation management
"""

from sqlalchemy.orm import Session
from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationResponse
from typing import List, Optional
from datetime import date, time


class ReservationService:
    """Service for managing reservations"""

    def create_reservation(
        self,
        db: Session,
        reservation_data: ReservationCreate
    ) -> Reservation:
        """Create new reservation"""

        # Get or create user
        if reservation_data.user_id:
            user = db.query(User).filter(User.id == reservation_data.user_id).first()
            if not user:
                raise ValueError(f"User with ID {reservation_data.user_id} not found")
            user_id = user.id
        elif reservation_data.phone_number:
            user = db.query(User).filter(User.phone_number == reservation_data.phone_number).first()
            if not user:
                user = User(phone_number=reservation_data.phone_number)
                db.add(user)
                db.flush()
            user_id = user.id
        else:
            raise ValueError("Either user_id or phone_number is required")

        # Create reservation
        reservation = Reservation(
            user_id=user_id,
            reservation_date=reservation_data.reservation_date,
            reservation_time=reservation_data.reservation_time,
            party_size=reservation_data.party_size,
            status=ReservationStatus.PENDING,
            special_requests=reservation_data.special_requests
        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    def get_reservation(
        self,
        db: Session,
        reservation_id: int
    ) -> Optional[Reservation]:
        """Get reservation by ID"""
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def get_user_reservations(
        self,
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[Reservation]:
        """Get reservations for a user"""
        return db.query(Reservation).filter(
            Reservation.user_id == user_id
        ).order_by(
            Reservation.reservation_date.desc()
        ).limit(limit).all()

    def update_reservation_status(
        self,
        db: Session,
        reservation_id: int,
        new_status: str
    ) -> Reservation:
        """Update reservation status"""
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

        if not reservation:
            raise ValueError(f"Reservation {reservation_id} not found")

        # Validate status
        try:
            status_enum = ReservationStatus(new_status.lower())
        except ValueError:
            raise ValueError(f"Invalid status: {new_status}")

        reservation.status = status_enum
        db.commit()
        db.refresh(reservation)

        return reservation

    def cancel_reservation(
        self,
        db: Session,
        reservation_id: int
    ) -> Reservation:
        """Cancel a reservation"""
        return self.update_reservation_status(db, reservation_id, "cancelled")

    def format_reservation_response(
        self,
        reservation: Reservation
    ) -> ReservationResponse:
        """Format reservation for API response"""
        return ReservationResponse(
            id=reservation.id,
            user_id=reservation.user_id,
            reservation_date=reservation.reservation_date.isoformat(),
            reservation_time=reservation.reservation_time.isoformat(),
            party_size=reservation.party_size,
            status=reservation.status.value,
            special_requests=reservation.special_requests,
            created_at=reservation.created_at.isoformat()
        )

    def generate_reservation_summary(
        self,
        reservation: Reservation
    ) -> str:
        """Generate human-readable reservation summary"""
        lines = [
            f"📅 **Reservation #{reservation.id}**",
            f"Status: {reservation.status.value.upper()}",
            f"",
            f"📆 Date: {reservation.reservation_date.strftime('%B %d, %Y')}",
            f"🕐 Time: {reservation.reservation_time.strftime('%I:%M %p')}",
            f"👥 Party Size: {reservation.party_size} people",
        ]

        if reservation.special_requests:
            lines.append(f"📝 Special Requests: {reservation.special_requests}")

        return "\n".join(lines)


# Create singleton instance
reservation_service = ReservationService()
