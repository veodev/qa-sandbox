from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import CarIn, CarOut
from services import cars as cars_service

router = APIRouter(prefix="/cars", tags=["cars"])


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
