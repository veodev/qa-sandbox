from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import cars as cars_repo
from repositories import users as users_repo


async def create_car(db: AsyncSession, user_id: UUID, brand: str, model: str, year: int, mileage: int) -> Car:
    user = await users_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await cars_repo.create(db, user_id, brand, model, year, mileage)
