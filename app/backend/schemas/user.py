from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
