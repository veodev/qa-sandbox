from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import Car


async def create(db: AsyncSession, user_id: UUID, brand: str, model: str, year: int, mileage: int) -> Car:
    car = Car(user_id=user_id, brand=brand, model=model, year=year, mileage=mileage)
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return car
