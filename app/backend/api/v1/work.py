from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import WorkIn, WorkOut
from services import work as work_service

router = APIRouter(prefix="/works", tags=["works"])


@router.get("", response_model=list[WorkOut])
async def get_works(db: AsyncSession = Depends(get_db)):
    return await work_service.get_all_works(db)


@router.get("/{work_id}", response_model=WorkOut)
async def get_work(work_id: UUID, db: AsyncSession = Depends(get_db)):
    return await work_service.get_work_by_id(db, work_id)


@router.get("/car/{car_id}", response_model=list[WorkOut])
async def get_works_by_car(car_id: UUID, db: AsyncSession = Depends(get_db)):
    return await work_service.get_works_by_car(db, car_id)


@router.post("", response_model=WorkOut, status_code=status.HTTP_201_CREATED)
async def create_work(work_data: WorkIn, db: AsyncSession = Depends(get_db)):
    return await work_service.create_work(
        db=db,
        car_id=work_data.car_id,
        description=work_data.description,
        mileage=work_data.mileage,
        cost=work_data.cost,
        performed_date=work_data.performed_date,
    )


@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_work(work_id: UUID, db: AsyncSession = Depends(get_db)):
    return await work_service.remove_work(db, work_id)
