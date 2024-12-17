from fastapi import (
    APIRouter,
    Depends,
)

from app.message.dependence import get_message_service
from app.message.services import IMessageService
from app.message.schemas import Message


router = APIRouter(prefix="/message")


@router.get("/message")
async def get_messages(
    service: IMessageService = Depends(get_message_service),
) -> list[Message]:
    messages = await service.get_messages()
    return messages
