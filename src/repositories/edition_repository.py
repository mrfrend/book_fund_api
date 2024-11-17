from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from schemas.schemas import *
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

    def get(self, id: int):
        with self.db_session() as session:
            query = (
                session.query(Edition)
                .options(
                    joinedload(Edition.book).selectinload(Book.genres),
                    joinedload(Edition.book).selectinload(Book.authors),
                    joinedload(Edition.book).joinedload(Book.country),
                    joinedload(Edition.publisher),
                    joinedload(Edition.language),
                )
                .where(Edition.id == id)
            )
            result = session.execute(query).scalar()
            return EditionRelDTO.model_validate(result, from_attributes=True)

    def get_all(self):
        with self.db_session() as session:
            query = session.query(Edition).options(
                joinedload(Edition.book).selectinload(Book.genres),
                joinedload(Edition.book).selectinload(Book.authors),
                joinedload(Edition.book).joinedload(Book.country),
                joinedload(Edition.publisher),
                joinedload(Edition.language),
            )

            result = session.execute(query).unique().scalars().all()
            editions_rel_dto = [
                EditionRelDTO.model_validate(row, from_attributes=True)
                for row in result
            ]
            return editions_rel_dto
