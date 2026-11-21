from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class WorkIn(BaseModel):
    car_id: UUID
    description: str = Field(..., min_length=1, max_length=500)
    mileage: int = Field(..., ge=0)
    cost: float = Field(..., ge=0)
    performed_date: date


class WorkOut(BaseModel):
    id: UUID
    car_id: UUID
    description: str
    mileage: int
    cost: float
    performed_date: date
