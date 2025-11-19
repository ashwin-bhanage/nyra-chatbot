"""
Reservation Model - Represents table reservations
"""

from sqlalchemy import Column, Integer, Date, Time, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ReservationStatus(str, enum.Enum):
    """Possible reservation statuses"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Reservation(Base):
    """
    Reservation table - stores table reservations

    Relationships:
    - user: The customer who made the reservation
    """

    __tablename__ = "reservations"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Reservation details
    reservation_date = Column(Date, nullable=False, index=True)
    reservation_time = Column(Time, nullable=False)
    party_size = Column(Integer, nullable=False)  # Number of people

    # Status
    status = Column(
        Enum(ReservationStatus),
        default=ReservationStatus.PENDING,
        nullable=False,
        index=True
    )

    # Optional requests
    special_requests = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="reservations")

    def __repr__(self):
        """String representation for debugging"""
        return f"<Reservation(id={self.id}, date={self.reservation_date}, time={self.reservation_time}, party={self.party_size})>"
