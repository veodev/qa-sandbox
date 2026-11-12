from uuid import UUID

from pydantic import BaseModel


class CarIn(BaseModel):
    user_id: UUID
    brand: str
    model: str
    year: int
    mileage: int = 0


class CarOut(BaseModel):
    id: UUID
    user_id: UUID
    brand: str
    model: str
    year: int
    mileage: int
