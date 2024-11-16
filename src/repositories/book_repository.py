from typing import Union
from schemas.schemas import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from database.models import Book, Genre, Author, Catalog, Edition
from database.database import session_factory
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(
            model=Book,
            db_session=session_factory,
        )

    def get_all(self) -> list[Book]:
        with self.db_session() as session:
            query = (
                select(Book)
                .options(selectinload(Book.genres))
                .options(selectinload(Book.authors))
                .options(selectinload(Book.catalogs))
                .options(selectinload(Book.editions))
                .options(joinedload(Book.country))
            )
            execution = session.execute(query)
            result = execution.unique().scalars().all()
            return result

    def add_related_entities(
        self,
        book_id: int,
        entities: list[Union["Genre", "Author", "Catalog", "Edition"]],
        entity_attr: str,
    ):
        with self.db_session() as session:
            book: Book = session.get(Book, book_id)
            if book is None:
                return None

            getattr(book, entity_attr).extend(entities)

            session.commit()
            session.refresh(book)

            query = (
                select(Book)
                .options(selectinload(getattr(Book, entity_attr)))
                .where(Book.id == book_id)
            )

            execution = session.execute(query)
            result = execution.unique().scalar()
            return result

    def add_editions(self, book_id: int, editions: list[Edition]):
        with self.db_session() as session:
            book: Book | None = session.get(Book, book_id)
            if book is None:
                return None
            book.editions.extend(editions)
            session.commit()
            session.refresh(book)
            query = (
                select(Book)
                .options(joinedload(Book.editions))
                .where(Book.id == book_id)
            )
            execution = session.execute(query)
            result = execution.unique().scalar()
            return result

        # def add_genres(self, book_id: int, genres: list[Genre]):
        #     with self.db_session() as session:
        #         book: Book | None = session.get(Book, book_id)
        #         if book is None:
        #             return None
        #         book.genres.extend(genres)
        #         session.commit()
        #         session.refresh(book)
        #         query = (
        #             select(Book)
        #             .options(selectinload(Book.genres))
        #             .where(Book.id == book_id)
        #         )
        #         execution = session.execute(query)
        #         result = execution.unique().scalar()
        #         return result

        # def add_authors(self, book_id: int, authors: list[Author]):
        #     with self.db_session() as session:
        #         book: Book | None = session.get(Book, book_id)
        #         if book is None:
        #             return None
        #         book.authors.extend(authors)
        #         session.commit()
        #         session.refresh(book)
        #         query = (
        #             select(Book)
        #             .options(selectinload(Book.authors))
        #             .where(Book.id == book_id)
        #         )
        #         execution = session.execute(query)
        #         result = execution.unique().scalar()
        #         return result

        # def add_catalogs(self, book_id: int, catalogs: list[Catalog]):
        with self.db_session() as session:
            book: Book | None = session.get(Book, book_id)
            if book is None:
                return None
            book.authors.extend(catalogs)
            session.commit()
            session.refresh(book)
            query = (
                select(Book)
                .options(selectinload(Book.catalogs))
                .where(Book.id == book_id)
            )
            execution = session.execute(query)
            result = execution.unique().scalar()
            return result
