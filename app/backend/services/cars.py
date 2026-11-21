from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import Car
from repositories import cars as cars_repo
from repositories import users as users_repo


async def create_car(db: AsyncSession, user_id: UUID, brand: str, model: str, year: int, mileage: int) -> Car:
    user = await users_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await cars_repo.create(db, user_id, brand, model, year, mileage)


async def get_car_by_id(db: AsyncSession, car_id: UUID) -> Car:
    car = await cars_repo.get_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car


async def get_cars_by_user(db: AsyncSession, user_id: UUID) -> list[Car]:
    user = await users_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await cars_repo.get_by_user(db, user_id)


async def remove_car(db: AsyncSession, car_id: UUID):
    removed_count = await cars_repo.remove(db, car_id)
    if not removed_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")


async def get_all_cars(db: AsyncSession) -> list[Car]:
    return await cars_repo.get_all(db)
