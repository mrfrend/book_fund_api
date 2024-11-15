from repositories import *
from schemas.books import *
from schemas.editions import *
from services.base_service import BaseService


class BookService(BaseService[BookDTO, BookAddDTO, BookUpdateDTO]):
    def __init__(self):
        super().__init__(BookRepository, BookDTO, BookAddDTO, BookUpdateDTO)


class CatalogService(BaseService[CatalogDTO, CatalogAddDTO, CatalogAddDTO]):
    def __init__(self):
        super().__init__(CatalogRepository, CatalogDTO, CatalogAddDTO, CatalogAddDTO)


class AuthorService(BaseService[AuthorDTO, AuthorAddDTO, AuthorUpdateDTO]):
    def __init__(self):
        super().__init__(AuthorRepository, AuthorDTO, AuthorAddDTO, AuthorUpdateDTO)


class PublisherService(BaseService[PublisherDTO, PublisherAddDTO, PublisherAddDTO]):
    def __init__(self):
        super().__init__(
            PublisherRepository, PublisherDTO, PublisherAddDTO, PublisherAddDTO
        )


class EditionService(BaseService[EditionDTO, EditionAddDTO, EditionUpdateDTO]):
    def __init__(self):
        super().__init__(EditionRepository, EditionDTO, EditionAddDTO, EditionUpdateDTO)


class GenreService(BaseService[GenreDTO, GenreAddDTO, GenreAddDTO]):
    def __init__(self):
        super().__init__(GenreRepository, GenreDTO, GenreAddDTO, GenreAddDTO)


class LanguageService(BaseService[LanguageDTO, LanguageAddDTO, LanguageAddDTO]):
    def __init__(self):
        super().__init__(
            LanguageRepository, LanguageDTO, LanguageAddDTO, LanguageAddDTO
        )


class CountryService(BaseService[CountryDTO, CountryAddDTO, CountryAddDTO]):
    def __init__(self):
        super().__init__(CountryRepository, CountryDTO, CountryAddDTO, CountryAddDTO)
