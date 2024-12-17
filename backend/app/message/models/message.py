from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ...core.db.base import Base


class Message(Base):
    mid: Mapped[int] = mapped_column(Integer, unique=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    priority: Mapped[str] = mapped_column(
        String,
        default="Обычное",
        server_default="Обычное",
        nullable=False,
    )
    subject: Mapped[str | None] = mapped_column(String, nullable=True)
    body: Mapped[str | None] = mapped_column(String, nullable=True)
    read_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
