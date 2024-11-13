from typing import Generic, TypeVar, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)


class BaseRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]
):
    def __init__(
        self,
        model: ModelType,
        db_session: Session,
        return_dto: ReturnSchemaType,
        create_dto: CreateSchemaType,
        update_dto: UpdateSchemaType,
    ):
        self.model = model
        self.db_session: Session = db_session
        self.return_dto = return_dto
        self.create_dto = create_dto
        self.update_dto = update_dto

    def get_all(self) -> List[ReturnSchemaType]:
        with self.db_session() as session:
            query = select(self.model)
            result = session.execute(query).scalars().all()
            result_dto = [
                self.return_dto.model_validate(row, from_attributes=True)
                for row in result
            ]
            return result_dto

    def get(self, id: int) -> None | ReturnSchemaType:
        with self.db_session() as session:
            result = session.get(self.model, id)
            if result:
                result_dto = self.return_dto.model_validate(
                    result, from_attributes=True
                )
                return result_dto
            return None

    def create(self, data: CreateSchemaType) -> ReturnSchemaType:
        with self.db_session() as session:
            result = self.model(**data.model_dump())
            session.add(result)
            session.commit()
            session.refresh(result)
            result_dto = self.return_dto.model_validate(result, from_attributes=True)
            return result_dto

    def delete(self, id: int) -> 1 | 0:
        with self.db_session() as session:
            result = session.get(self.model, id)
            if result:
                session.delete(result)
                session.commit()
                return 1
            return 0

    def update(self, id: int, data: UpdateSchemaType) -> ReturnSchemaType | None:
        with self.db_session() as session:
            result = session.get(self.model, id)
            if result:
                for attr, value in data.model_dump(exclude_unset=True).items():
                    setattr(result, attr, value)
                session.commit()
                session.refresh(result)
                result_dto = self.return_dto.model_validate(
                    result, from_attributes=True
                )
                return result_dto
            return None
