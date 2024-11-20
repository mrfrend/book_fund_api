from typing import Generic, TypeVar
from pydantic import BaseModel
from repositories.base_repository import BaseRepository

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReturnSchema = TypeVar("ReturnSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseService(Generic[ReturnSchema, CreateSchema, UpdateSchema]):
    def __init__(
        self,
        repository: BaseRepository,
        result_dto: ReturnSchema,
        create_dto: CreateSchema,
        update_dto: UpdateSchema,
    ) -> None:
        self.repository = repository()
        self.result_dto = result_dto
        self.create_dto = create_dto
        self.update_dto = update_dto

    def get_all(self) -> list[ReturnSchema]:
        data = self.repository.get_all()
        result = [
            self.result_dto.model_validate(row, from_attributes=True) for row in data
        ]
        return result

    def get(self, id: int) -> ReturnSchema:
        model = self.repository.get(id=id)
        model_dto = self.result_dto.model_validate(model, from_attributes=True)
        return model_dto

    def create(self, data: CreateSchema) -> ReturnSchema:
        model = self.repository.create(data)
        model_dto = self.result_dto.model_validate(model, from_attributes=True)
        return model_dto

    def delete(self, id: int) -> bool | None:
        return self.repository.delete(id=id)

    def update(self, id: int, data: UpdateSchema) -> ReturnSchema:
        return self.repository.update(id=id, data=data)
