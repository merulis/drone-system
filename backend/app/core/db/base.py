from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}: {str(self.__dict__)}"

    def __repr__(self):
        return str(self)
