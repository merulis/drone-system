from sqlalchemy.orm import Session

from app.core.db import sync_db

from app.message.models.message import Message
from app.gonets.repositories import GonetsMessage

from app.gonets.repositories.interface import (
    ICeleryBackendRepository,
)


class GonetsRepository(ICeleryBackendRepository[Message, GonetsMessage]):
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        obj_in: GonetsMessage,
    ) -> Message:
        record = obj_in.model_dump(by_alias=False)
        message = Message(**record)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def create_many(
        self,
        obj_list_in: list[GonetsMessage],
    ) -> list[Message]:
        records = [obj.model_dump(by_alias=False) for obj in obj_list_in]
        messages = [Message(**record) for record in records]
        self.session.add_all(messages)
        self.session.commit()
        return messages


def get_gonets_repository():
    session = sync_db.session_dependency()
    return GonetsRepository(session=session)
