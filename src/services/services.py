from fastapi import UploadFile
from database.models import Book, Genre
from repositories import *
from schemas import *
import asyncio
from schemas.book_schemas import BookUpdateFrontDTO
from services.base_service import BaseService
from repositories.genre_repository import GenreRepository
from repositories.author_repository import AuthorRepository
from repositories.catalog_repository import CatalogRepository


class BookService(BaseService[BookDTO, BookAddDTO, BookUpdateDTO]):
    def __init__(self):
        super().__init__(BookRepository, BookDTO, BookAddDTO, BookUpdateDTO)

    async def update(
        self, id: int, data: BookUpdateFrontDTO, image: UploadFile = None
    ) -> BookRelDTO:
        await self.repository.update(id, data, image)
        catalogs, authors, genres = await asyncio.gather(
            CatalogRepository().get_specific_catalogs(data.catalogs),
            AuthorRepository().get_specific_authors(data.authors),
            GenreRepository().get_specific_genres(data.genres),
        )
        updated_book = await self.repository.update_entities_to_book(
            id, catalogs, authors, genres
        )
        return updated_book

    async def create(self, data: BookAddDTO, image: UploadFile) -> BookRelDTO:
        created_book_id = await self.repository.create(data, image)
        catalogs, authors, genres = await asyncio.gather(
            CatalogRepository().get_specific_catalogs(data.catalogs),
            AuthorRepository().get_specific_authors(data.authors),
            GenreRepository().get_specific_genres(data.genres),
        )
        updated_book = await self.repository.add_entities_to_book(
            created_book_id, catalogs, authors, genres
        )
        print("updated_book", updated_book)
        return updated_book

    async def get_image_book(self, book_id: int) -> tuple[bytes, str]:
        image_content, image_path = await self.repository.get_image_book(book_id)
        return (image_content, image_path)

    async def get(self, book_id: int) -> BookRelDTO:
        data = await self.repository.get(book_id)
        result = BookRelDTO.model_validate(data, from_attributes=True)
        return result

    async def get_all(self) -> list[BookRelDTO]:
        data = await self.repository.get_all()
        result = [BookRelDTO.model_validate(row, from_attributes=True) for row in data]
        return result

    async def add_genres(self, book_id: int, genres: list[str]) -> list["BookGenreDTO"]:
        genre_models: list[Genre] = await GenreRepository().get_specific_genres(genres)
        updated_book = await self.repository.add_related_entities(
            book_id, genre_models, "genres"
        )
        book_genre_dto = BookGenreDTO.model_validate(updated_book, from_attributes=True)
        return book_genre_dto

    async def add_authors(self, book_id: int, authors_id: list[int]) -> BookAuthorDTO:
        authors_models = await AuthorRepository().get_specific_authors(authors_id)
        updated_book = await self.repository.add_related_entities(
            book_id, authors_models, "authors"
        )
        book_author_dto = BookAuthorDTO.model_validate(
            updated_book, from_attributes=True
        )
        return book_author_dto

    async def add_catalogs(
        self, book_id: int, catalogs: list[str]
    ) -> list["BookCatalogDTO"]:
        catalog_models = await CatalogRepository().get_specific_catalogs(catalogs)
        updated_book = await self.repository.add_related_entities(
            book_id, catalog_models, "catalogs"
        )
        book_catalog_dto = BookCatalogDTO.model_validate(
            updated_book, from_attributes=True
        )
        return book_catalog_dto

    async def get_desired_books(self, user_id: int) -> list["BookRelDTO"]:
        books_id = await self.repository.get_desired_books_id(user_id)
        books = await self.repository.get_specific_books(books_id)
        result = [
            BookRelDTO.model_validate(book, from_attributes=True) for book in books
        ]
        return result


class CatalogService(BaseService[CatalogDTO, CatalogAddDTO, CatalogAddDTO]):
    def __init__(self):
        super().__init__(CatalogRepository, CatalogDTO, CatalogAddDTO, CatalogAddDTO)


class AuthorService(BaseService[AuthorDTO, AuthorAddDTO, AuthorUpdateDTO]):
    def __init__(self):
        super().__init__(AuthorRepository, AuthorDTO, AuthorAddDTO, AuthorUpdateDTO)

    async def get_books_by_author_id(self, author_id: int) -> list["BookDTO"]:
        data = await self.repository.get_books_by_author_id(author_id)
        books_dto = [
            BookDTO.model_validate(book, from_attributes=True) for book in data.books
        ]
        return books_dto


class PublisherService(BaseService[PublisherDTO, PublisherAddDTO, PublisherAddDTO]):
    def __init__(self):
        super().__init__(
            PublisherRepository, PublisherDTO, PublisherAddDTO, PublisherAddDTO
        )


class GenreService(BaseService[GenreDTO, GenreAddDTO, GenreAddDTO]):
    def __init__(self):
        super().__init__(GenreRepository, GenreDTO, GenreAddDTO, GenreAddDTO)

    async def get_books_by_genre_id(self, genre_id: int):
        data = await self.repository.get_books_by_genre_id(genre_id)
        books_dto = [
            BookDTO.model_validate(book, from_attributes=True) for book in data.books
        ]
        return books_dto


# class LanguageService(BaseService[LanguageDTO, LanguageAddDTO, LanguageAddDTO]):
#     def __init__(self):
#         super().__init__(
#             LanguageRepository, LanguageDTO, LanguageAddDTO, LanguageAddDTO
#         )


class CountryService(BaseService[CountryDTO, CountryAddDTO, CountryAddDTO]):
    def __init__(self):
        super().__init__(CountryRepository, CountryDTO, CountryAddDTO, CountryAddDTO)


# class EditionService(BaseService[EditionDTO, EditionAddDTO, EditionUpdateDTO]):
#     def __init__(self):
#         super().__init__(EditionRepository, EditionDTO, EditionAddDTO, EditionUpdateDTO)

#     async def get_all(self) -> list[EditionRelDTO]:
#         editions = await self.repository.get_all()
#         return editions
