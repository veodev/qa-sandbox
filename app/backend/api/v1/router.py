from fastapi import APIRouter

from api.v1 import cars, users

router = APIRouter(prefix="/v1")
router.include_router(users.router)
router.include_router(cars.router)
