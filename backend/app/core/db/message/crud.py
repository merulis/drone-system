from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import Message


async def create_message(session: AsyncSession, schema):
    new_message = Message(schema)
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)
    return new_message
