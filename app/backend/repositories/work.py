from datetime import date
from typing import cast
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from models import Work


async def get_by_id(db: AsyncSession, work_id: UUID) -> Work | None:
    result = await db.execute(select(Work).where(Work.id == work_id))
    return result.scalar_one_or_none()


async def get_by_car(db: AsyncSession, car_id: UUID) -> list[Work]:
    result = await db.execute(select(Work).where(Work.car_id == car_id).order_by(Work.performed_date.desc()))
    return list(result.scalars().all())


async def get_all(db: AsyncSession) -> list[Work]:
    result = await db.execute(select(Work))
    return list(result.scalars().all())


async def create(db: AsyncSession, car_id: UUID, description: str, mileage: int, cost: float, performed_date: date) -> Work:
    work = Work(car_id=car_id, description=description, mileage=mileage, cost=cost, performed_date=performed_date)
    db.add(work)
    await db.commit()
    await db.refresh(work)
    return work


async def remove(db: AsyncSession, work_id: UUID) -> int:
    query = delete(Work).where(Work.id == work_id)
    result: CursorResult = cast(CursorResult, await db.execute(query))
    await db.commit()
    return result.rowcount
