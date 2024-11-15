from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: ModelType,
        db_session: Session,
    ):
        self.model = model
        self.db_session: Session = db_session

    def get_all(self) -> list[ModelType] | list:
        with self.db_session() as session:
            query = select(self.model)
            result = session.execute(query).scalars().all()
            return result

    def get(self, id: int) -> None | ModelType:
        with self.db_session() as session:
            result = session.get(self.model, id)
            return result

    def create(self, data) -> ModelType:
        with self.db_session() as session:
            result = self.model(**data.model_dump())
            session.add(result)
            session.commit()
            session.refresh(result)
            return result

    def delete(self, id: int) -> None:
        with self.db_session() as session:
            result = session.get(self.model, id)
            session.delete(result)
            session.commit()

    def update(self, id: int, data) -> ModelType | None:
        with self.db_session() as session:
            result = session.get(self.model, id)
            if result:
                for attr, value in data.model_dump(exclude_unset=True).items():
                    setattr(result, attr, value)
                session.commit()
                session.refresh(result)
                return result
            return None
