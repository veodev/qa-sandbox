from typing import cast
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from models import Car


async def get_by_id(db: AsyncSession, car_id: UUID) -> Car | None:
    result = await db.execute(select(Car).where(Car.id == car_id))
    return result.scalar_one_or_none()


async def get_by_user(db: AsyncSession, user_id: UUID) -> list[Car]:
    result = await db.execute(select(Car).where(Car.user_id == user_id))
    return list(result.scalars().all())


async def get_all(db: AsyncSession) -> list[Car]:
    result = await db.execute(select(Car))
    return list(result.scalars().all())


async def create(db: AsyncSession, user_id: UUID, brand: str, model: str, year: int, mileage: int) -> Car:
    car = Car(user_id=user_id, brand=brand, model=model, year=year, mileage=mileage)
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return car


async def remove(db: AsyncSession, car_id: UUID) -> int:
    query = delete(Car).where(Car.id == car_id)
    result: CursorResult = cast(CursorResult, await db.execute(query))
    await db.commit()
    return result.rowcount
