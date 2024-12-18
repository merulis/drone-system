from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.message.models.message import Message
from app.message.schemas.message import MessageCreate

from app.message.repositories.interface import IRepository


class MessageRepository(IRepository[Message, MessageCreate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        obj_in: MessageCreate,
    ) -> Message:
        record = obj_in.model_dump(by_alias=False)
        new_message = Message(**record)
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return new_message

    async def get_all_by_filter(
        self,
        **filters,
    ) -> list[Message]:
        stmt = select(Message).order_by(Message.id)
        result: Result = await self.session.execute(stmt)
        messages = list(result.scalars().all())
        return messages

    async def get_one_by_filter(
        self,
        id: int | None = None,
    ) -> Message | None:
        stmt = select(Message)

        if id:
            stmt = stmt.where(Message.id == id)
        else:
            return None

        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(
        self,
        obj: Message,
    ) -> None:
        await self.session.delete(obj)
        await self.session.commit()
