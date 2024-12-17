from app.message.schemas.message import Message, MessageCreate

from app.message.services.service_interface import IMessageService
from app.message.repositories.repository_interface import IRepository


class MessageService(IMessageService):
    def __init__(self, repository: IRepository):
        self.repository = repository

    async def create_message(
        self,
        message: MessageCreate,
    ) -> Message:
        result = await self.repository.create(
            message=message,
        )
        new_message = Message.model_validate(result)
        return new_message

    async def get_messages(
        self,
    ) -> list[Message]:
        result = await self.repository.get_all_by_filter()
        messages = [Message.model_validate(message) for message in result]
        return messages

    async def get_message_or_none(
        self,
        id: int | None = None,
        mid: int | None = None,
    ) -> Message | None:
        result = await self.repository.get_one_by_filter(
            id=id,
        )
        message = Message.model_validate(result)
        return message

    async def delete_message(
        self,
        message: Message,
    ) -> None:
        self.repository.delete(
            obj=message,
        )
