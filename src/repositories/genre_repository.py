from schemas.undepended_schemas import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.models import Genre, Book
from database.database import async_session_factory
from .base_repository import BaseRepository


class GenreRepository(BaseRepository[Genre]):
    def __init__(self):
        super().__init__(
            model=Genre,
            db_session=async_session_factory,
        )

    async def get_specific_genres(self, genres: list[str]) -> list[Genre]:
        genres = [int(genre_id) for genre_id in genres]
        async with self.db_session() as session:
            query = select(Genre).where(Genre.id.in_(genres))
            result = (await session.execute(query)).scalars().all()
            return result

    async def get_books_by_genre_id(self, genre_id: int) -> list[Book]:
        async with self.db_session() as session:
            query = (
                select(Genre)
                .options(selectinload(Genre.books))
                .where(Genre.id == genre_id)
            )
            result = await session.execute(query).unique().scalar()
            return result
