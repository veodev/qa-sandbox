from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
