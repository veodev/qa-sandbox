from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import users as users_repo
from security import get_password_hash


async def create_user(db: AsyncSession, email: str, name: str, password: str) -> User:
    if await users_repo.get_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed_pwd = get_password_hash(password)

    try:
        return await users_repo.create(db, email, name, hashed_pwd)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from None


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User:
    user = await users_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
