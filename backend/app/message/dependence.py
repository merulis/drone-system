from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_db
from app.message.repositories.repository import MessageRepository
from app.message.repositories.repository_interface import IRepository
from app.message.services.service import MessageService
from app.message.services.service_interface import IMessageService


def get_message_repository(
    session: AsyncSession = Depends(async_db.scoped_session_dependency),
) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
    repository: IRepository = Depends(get_message_repository),
) -> IMessageService:
    return MessageService(repository)
