from database.models import Genre
from repositories import *
from schemas import *
from services.base_service import BaseService


class BookService(BaseService[BookDTO, BookAddDTO, BookUpdateDTO]):
    def __init__(self):
        super().__init__(BookRepository, BookDTO, BookAddDTO, BookUpdateDTO)

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

    # async def add_editions(self, book_id: int, editions_id: list[str]):
    #     editions_models = await EditionRepository().get_specific_editions(editions_id)
    #     updated_book = await self.repository.add_related_entities(
    #         book_id, editions_models, "editions"
    #     )
    #     edition_rel_dto = EditionRelDTO.model_validate(
    #         updated_book, from_attributes=True
    #     )
    #     return edition_rel_dto


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