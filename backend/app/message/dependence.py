from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_db
from .repositories.repository import MessageRepository
from .repositories.interface import IRepository
from .services.service import MessageService
from .services.interface import IMessageService


def get_message_repository(
    session: AsyncSession = Depends(async_db.session_dependency),
) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
    repository: IRepository = Depends(get_message_repository),
) -> IMessageService:
    return MessageService(repository)
