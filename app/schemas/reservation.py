"""
Pydantic schemas for Reservation operations
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time
from typing import List  


class ReservationCreate(BaseModel):
    """Schema for creating reservation"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = Field(None, description="Phone number if user not registered")
    reservation_date: date = Field(..., description="Reservation date (YYYY-MM-DD)")
    reservation_time: time = Field(..., description="Reservation time (HH:MM)")
    party_size: int = Field(..., gt=0, le=20, description="Number of people (1-20)")
    special_requests: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+1234567890",
                "reservation_date": "2025-11-15",
                "reservation_time": "19:00",
                "party_size": 4,
                "special_requests": "Window seat preferred"
            }
        }


class ReservationUpdate(BaseModel):
    """Schema for updating reservation"""
    reservation_date: Optional[date] = None
    reservation_time: Optional[time] = None
    party_size: Optional[int] = Field(None, gt=0, le=20)
    special_requests: Optional[str] = None
    status: Optional[str] = None


class ReservationResponse(BaseModel):
    """Schema for reservation in response"""
    id: int
    user_id: Optional[int]
    reservation_date: str
    reservation_time: str
    party_size: int
    status: str
    special_requests: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "reservation_date": "2025-11-15",
                "reservation_time": "19:00:00",
                "party_size": 4,
                "status": "confirmed",
                "special_requests": "Window seat",
                "created_at": "2025-11-09T15:30:00"
            }
        }


class ReservationListResponse(BaseModel):
    """Schema for list of reservations"""
    reservations: List[ReservationResponse]
    total: int
