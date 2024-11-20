from schemas.undepended_schemas import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.models import Genre, Book
from database.database import session_factory
from .base_repository import BaseRepository


class GenreRepository(BaseRepository[Genre]):
    def __init__(self):
        super().__init__(
            model=Genre,
            db_session=session_factory,
        )

    def get_specific_genres(self, genres: list[str]) -> list[Genre]:
        with self.db_session() as session:
            query = select(Genre).where(Genre.name.in_(genres))
            result = session.execute(query).scalars().all()
            return result

    def get_books_by_genre_id(self, genre_id: int) -> list[Book]:
        with self.db_session() as session:
            query = (
                select(Genre)
                .options(selectinload(Genre.books))
                .where(Genre.id == genre_id)
            )
            result = session.execute(query).unique().scalar()
            return result
