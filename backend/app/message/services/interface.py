from abc import ABC, abstractmethod
from typing import List, Optional

from app.message.schemas.message import Message, MessageCreate


class IMessageService(ABC):
    @abstractmethod
    async def create_message(
        self,
        message: MessageCreate,
    ) -> Message:
        pass

    @abstractmethod
    async def get_messages(
        self,
    ) -> List[Message]:
        pass

    @abstractmethod
    async def get_message_or_none(
        self,
        id: Optional[int] = None,
        mid: Optional[int] = None,
    ) -> Optional[Message]:
        pass

    @abstractmethod
    async def delete_message(
        self,
        message: Message,
    ) -> None:
        pass
