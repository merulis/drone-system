import logging
import traceback

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.message.dependence import get_message_service
from app.message.services import IMessageService
from app.message.schemas import Message


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

router = APIRouter(prefix="/message")


@router.get("/")
async def get_messages(
    service: IMessageService = Depends(get_message_service),
) -> list[Message]:
    try:
        messages = await service.get_messages()
    except Exception as e:
        logger.error(f"failed to retrieve message: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    else:
        return messages
