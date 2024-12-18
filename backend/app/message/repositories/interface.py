from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")


class IRepository(ABC, Generic[ModelType, CreateSchemaType]):
    @abstractmethod
    async def create(
        self,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        pass

    @abstractmethod
    async def get_all_by_filter(
        self,
        **filters,
    ) -> List[ModelType]:
        pass

    @abstractmethod
    async def get_one_by_filter(
        self,
        id: int,
        **filters,
    ) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def delete(
        self,
        obj: ModelType,
    ) -> None:
        pass
