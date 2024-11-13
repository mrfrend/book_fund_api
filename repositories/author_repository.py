from schemas.books import *
from sqlalchemy import select
from database.models import Author
from schemas.books import AuthorDTO, AuthorAddDTO
from database.database import session_factory


class AuthorRepository:
    @classmethod
    def get_authors(cls) -> list[AuthorDTO]:
        with session_factory() as session:
            query = select(Author)
            res = session.execute(query).scalars().all()
            authors_dto = [
                AuthorDTO.model_validate(author, from_attributes=True) for author in res
            ]
            return authors_dto

    @classmethod
    def get_author(cls, author_id: int) -> AuthorDTO | None:
        with session_factory() as session:
            author = session.get(Author, author_id)
            if author is None:
                return None
            return AuthorDTO.model_validate(author, from_attributes=True)

    @classmethod
    def add_author(cls, data: AuthorAddDTO) -> int:
        with session_factory() as session:
            author_dict = data.model_dump()
            author = Author(**author_dict)
            session.add(author)
            session.commit()
            session.refresh(author)
            return author.id

    @classmethod
    def delete_author(cls, author_id: int) -> 0 | 1:
        with session_factory() as session:
            query = select(Author).where(Author.id == author_id)
            author = session.execute(query).scalar_one_or_none()
            if author:
                session.delete(author)
                session.commit()
                return 1
            return 0
