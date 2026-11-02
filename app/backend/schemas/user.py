from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateUserIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class CreateUserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
