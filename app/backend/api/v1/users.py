from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import UserIn, UserOut
from services import users as users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserIn, db: AsyncSession = Depends(get_db)):
    return await users_service.create_user(db=db, email=new_user.email, name=new_user.name, password=new_user.password)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await users_service.get_user_by_id(db, user_id)
