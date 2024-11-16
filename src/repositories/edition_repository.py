from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from schemas.books_schema import *
from database.models import Edition, Book
from database.database import session_factory
from .base_repository import BaseRepository


class EditionRepository(BaseRepository[Edition]):
    def __init__(self):
        super().__init__(
            model=Edition,
            db_session=session_factory,
        )

    def get_specific_editions(self, editions_id: list[int]) -> list[Edition]:
        with self.db_session() as session:
            query = select(Edition).where(Edition.id.in_(editions_id))
            result = session.execute(query).scalars().all()
            return result

    def get_all(self):
        with self.db_session() as session:
            query = (
                select(Edition)
                .options(
                    joinedload(Edition.book)
                    .selectinload(Book.authors)
                    .selectinload(Book.catalogs)
                    .selectinload(Book.genres)
                    .joinedload(Book.country)
                )
                .options(joinedload(Edition.publisher).joinedload(Edition.language))
            )

            result = session.execute(query).unique().scalars().all()
            return result
