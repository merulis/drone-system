from fastapi import APIRouter

from .routes.message import router as message

router = APIRouter()

router.include_router(router=message, tags=["Message"])
