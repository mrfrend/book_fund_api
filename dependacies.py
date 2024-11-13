from repositories.author_repository import AuthorRepository
from repositories.catalog_repository import CatalogRepository
from repositories.country_repository import CountryRepository
from repositories.genre_repository import GenreRepository
from repositories.language_repository import LanguageRepository
from repositories.publisher_repository import PublisherRepository
from repositories.book_repository import BookRepository


def get_author_repository():
    return AuthorRepository()


def get_catalog_repository():
    return CatalogRepository()


def get_country_repository():
    return CountryRepository()


def get_genre_repository():
    return GenreRepository()


def get_language_repository():
    return LanguageRepository()


def get_publisher_repository():
    return PublisherRepository()

def get_book_repository():
    return BookRepository()