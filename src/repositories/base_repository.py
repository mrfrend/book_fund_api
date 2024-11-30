from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: ModelType,
        db_session: AsyncSession,
    ):
        self.model = model
        self.db_session: AsyncSession = db_session

    async def get_all(self) -> list[ModelType] | list:
        async with self.db_session() as session:
            query = select(self.model)
            result = (await session.execute(query)).scalars().all()
            return result

    async def get(self, id: int) -> None | ModelType:
        async with self.db_session() as session:
            result = await session.get(self.model, id)
            return result

    async def create(self, data) -> ModelType:
        async with self.db_session() as session:
            result = self.model(**data.model_dump())
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result

    async def delete(self, id: int) -> bool | None:
        async with self.db_session() as session:
            result = await session.get(self.model, id)
            if result:
                await session.delete(result)
                await session.commit()
                return True
            return None

    async def update(self, id: int, data) -> ModelType | None:
        async with self.db_session() as session:
            result = await session.get(self.model, id)
            if result:
                for attr, value in data.model_dump(exclude_unset=True).items():
                    setattr(result, attr, value)
                await session.commit()
                await session.refresh(result)
                return result
            return None
