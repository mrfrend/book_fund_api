from typing import Union
from schemas.undepended_schemas import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from database.models import Book, Genre, Author, Catalog, Edition
from database.database import async_session_factory
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(
            model=Book,
            db_session=async_session_factory,
        )

    async def get_all(self) -> list[Book]:
        async with self.db_session() as session:
            query = (
                select(Book)
                .options(selectinload(Book.genres))
                .options(selectinload(Book.authors))
                .options(selectinload(Book.catalogs))
                .options(selectinload(Book.editions))
                .options(joinedload(Book.country))
            )
            print(query)
            execution = await session.execute(query)
            result = execution.unique().scalars().all()
            return result

    async def add_related_entities(
        self,
        book_id: int,
        entities: list[Union["Genre", "Author", "Catalog", "Edition"]],
        entity_attr: str,
    ):
        async with self.db_session() as session:
            book: Book = await session.get(Book, book_id)
            if book is None:
                return None

            getattr(book, entity_attr).extend(entities)

            await session.commit()
            await session.refresh(book)

            query = (
                select(Book)
                .options(selectinload(getattr(Book, entity_attr)))
                .where(Book.id == book_id)
            )

            execution = await session.execute(query)
            result = execution.unique().scalar()
            return result

    async def add_editions(self, book_id: int, editions: list[Edition]):
        async with self.db_session() as session:
            book: Book | None = await session.get(Book, book_id)
            if book is None:
                return None
            book.editions.extend(editions)
            await session.commit()
            await session.refresh(book)
            query = (
                select(Book)
                .options(joinedload(Book.editions))
                .where(Book.id == book_id)
            )
            execution = await session.execute(query)
            result = execution.unique().scalar()
            return result

        # async def add_genres(self, book_id: int, genres: list[Genre]):
        #     async with self.db_session() as session:
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

        # async def add_authors(self, book_id: int, authors: list[Author]):
        #     async with self.db_session() as session:
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

        # async def add_catalogs(self, book_id: int, catalogs: list[Catalog]):
        async with self.db_session() as session:
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
