from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")


class ICeleryBackendRepository(ABC, Generic[ModelType, CreateSchemaType]):
    @abstractmethod
    def create(
        self,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        pass

    @abstractmethod
    def create_many(
        self,
        obj_list_in: list[CreateSchemaType],
    ) -> list[ModelType]:
        pass
