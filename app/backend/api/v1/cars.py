from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import CarIn, CarOut
from services import cars as cars_service

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("", response_model=list[CarOut])
async def get_cars(db: AsyncSession = Depends(get_db)):
    return await cars_service.get_all_cars(db)


@router.get("/{car_id}", response_model=CarOut)
async def get_car(car_id: UUID, db: AsyncSession = Depends(get_db)):
    return await cars_service.get_car_by_id(db, car_id)


@router.post("", response_model=CarOut, status_code=status.HTTP_201_CREATED)
async def create_car(car_data: CarIn, db: AsyncSession = Depends(get_db)):
    return await cars_service.create_car(
        db=db,
        user_id=car_data.user_id,
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        mileage=car_data.mileage,
    )


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_car(car_id: UUID, db: AsyncSession = Depends(get_db)):
    return await cars_service.remove_car(db, car_id)
