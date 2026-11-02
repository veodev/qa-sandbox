from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import CreateUserIn, CreateUserOut
from services import users as users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=CreateUserOut, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: CreateUserIn, db: AsyncSession = Depends(get_db)):
    return await users_service.create_user(db=db, email=new_user.email, name=new_user.name, password=new_user.password)
