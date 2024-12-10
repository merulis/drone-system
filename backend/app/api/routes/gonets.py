from fastapi import APIRouter


router = APIRouter(prefix="/gonets")


@router.get("/message")
async def get_messages():
    pass
