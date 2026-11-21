from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import Work
from repositories import cars as cars_repo
from repositories import work as work_repo


async def create_work(db: AsyncSession, car_id: UUID, description: str, mileage: int, cost: float, performed_date: date) -> Work:
    car = await cars_repo.get_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return await work_repo.create(db, car_id, description, mileage, cost, performed_date)


async def get_work_by_id(db: AsyncSession, work_id: UUID) -> Work:
    work = await work_repo.get_by_id(db, work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    return work


async def get_works_by_car(db: AsyncSession, car_id: UUID) -> list[Work]:
    car = await cars_repo.get_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return await work_repo.get_by_car(db, car_id)


async def remove_work(db: AsyncSession, work_id: UUID):
    removed_count = await work_repo.remove(db, work_id)
    if not removed_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")


async def get_all_works(db: AsyncSession) -> list[Work]:
    return await work_repo.get_all(db)
