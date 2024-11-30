from database.models import Author
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.database import async_session_factory
from .base_repository import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(
            model=Author,
            db_session=async_session_factory,
        )

    async def get_specific_authors(self, authors_id: list[int]):
        async with self.db_session() as session:
            query = select(Author).where(Author.id.in_(authors_id))
            result = (await session.execute(query)).scalars().all()
            return result

    async def get_books_by_author_id(self, author_id: int):
        async with self.db_session() as session:
            query = (
                select(Author)
                .options(selectinload(Author.books))
                .where(Author.id == author_id)
            )
            result = (await session.execute(query)).unique().scalar()
            return result
