from fastapi import APIRouter

from api.v1 import users

router = APIRouter(prefix="/v1")
router.include_router(users.router)
