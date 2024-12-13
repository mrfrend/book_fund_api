from typing import Union
from fastapi import UploadFile
from schemas.undepended_schemas import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Book, Genre, Author, Catalog
from schemas import BookAddDTO
from database.database import async_session_factory
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(
            model=Book,
            db_session=async_session_factory,
        )
    
    async def write_image(self, image: UploadFile, book: Book):
        img_name = image.filename
        with open(f'images/{img_name}', 'wb') as buffer:
            buffer.write(await image.read())
            book.img_path = f'images/{img_name}'
    
    async def create(self, data: BookAddDTO, image: UploadFile) -> Book:
        async with self.db_session() as session:
            book_model= Book(**data.model_dump())
            session.add(book_model)
            await self.write_image(image, book_model)
            await session.commit()
            await session.refresh(book_model)
            return book_model

    async def get_image_book(self, book_id: int) -> tuple[bytes, str]:
        async with self.db_session() as session:
            book: Book = await session.get(Book, book_id)
            if book is None:
                return None
            with open(book.img_path, 'rb') as buffer:
                return (buffer.read(), book.img_path)


    async def get_all(self) -> list[Book]:
        async with self.db_session() as session:
            query = (
                select(Book)
                .options(selectinload(Book.genres))
                .options(selectinload(Book.authors))
                .options(selectinload(Book.catalogs))
                .options(joinedload(Book.publisher))
                .options(joinedload(Book.country))
            )
            execution = await session.execute(query)
            result = execution.unique().scalars().all()
            return result

    async def add_related_entities(
        self,
        book_id: int,
        entities: list[Union["Genre", "Author", "Catalog"]],
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

        # async def add_editions(self, book_id: int, editions: list[Edition]):
        #     async with self.db_session() as session:
        #         book: Book | None = await session.get(Book, book_id)
        #         if book is None:
        #             return None
        #         book.editions.extend(editions)
        #         await session.commit()
        #         await session.refresh(book)
        #         query = (
        #             select(Book)
        #             .options(joinedload(Book.editions))
        #             .where(Book.id == book_id)
        #         )
        #         execution = await session.execute(query)
        #         result = execution.unique().scalar()
        #         return result

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
        #     async with self.db_session() as session:
        #         book: Book | None = session.get(Book, book_id)
        #         if book is None:
        #             return None
        #         book.catalogs.extend(catalogs)
        #         session.commit()
        #         session.refresh(book)
        #     query = (
        #         select(Book)
        #         .options(selectinload(Book.catalogs))
        #         .where(Book.id == book_id)
        #     )
        #     execution = session.execute(query)
        #     result = execution.unique().scalar()
        #     return result
