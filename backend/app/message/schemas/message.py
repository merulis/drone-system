from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class MessageCreate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    mid: int
    timestamp: datetime
    priority: str
    subject: str
    body: str
    read_status: bool
    deleted: bool


class Message(MessageCreate):
    db_id: int
