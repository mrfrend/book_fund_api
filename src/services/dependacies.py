from services import *


def get_author_service():
    return AuthorService()


def get_catalog_service():
    return CatalogService()


def get_country_service():
    return CountryService()


def get_genre_service():
    return GenreService()


def get_language_service():
    return LanguageService()


def get_publisher_service():
    return PublisherService()


def get_book_service():
    return BookService()


def get_edition_service():
    return EditionService()
