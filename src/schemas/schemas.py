from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError, field_validator
from database.models import Status
import re
# from .editions import EditionDTO


class LanguageAddDTO(BaseModel):
    name: str = Field(max_length=25)


class LanguageDTO(LanguageAddDTO):
    id: int


class GenreAddDTO(BaseModel):
    name: str = Field(max_length=30)


class GenreDTO(GenreAddDTO):
    id: int


class AuthorAddDTO(BaseModel):
    first_name: str = Field(max_length=25, default="Иван")
    last_name: str = Field(max_length=50, default="Иванов")
    middle_name: str | None = Field(max_length=50, default=None)


class AuthorUpdateDTO(BaseModel):
    first_name: str | None = Field(max_length=25, default="Иван")
    last_name: str | None = Field(max_length=50, default="Иванов")
    middle_name: str | None = Field(max_length=50, default=None)


class AuthorDTO(AuthorAddDTO):
    id: int


class CatalogAddDTO(BaseModel):
    name: str = Field(max_length=50)


class CatalogDTO(CatalogAddDTO):
    id: int


class CountryAddDTO(BaseModel):
    name: str


class CountryDTO(CountryAddDTO):
    id: int


class BookAddDTO(BaseModel):
    title: str = Field(max_length=40)
    keywords: str | None = None
    year_released: int = Field(gt=0, lt=2025)
    description: str = Field(max_length=500)
    country_id: int = Field(gt=0)


class BookUpdateDTO(BaseModel):
    title: str | None = Field(max_length=40, default=None)
    keywords: str | None = None
    year_released: int | None = Field(gt=0, le=2024, default=None)
    description: str | None = Field(max_length=500, default=None)
    country_id: int | None = Field(gt=0, default=None)


class BookDTO(BookAddDTO):
    id: int


class BookGenreDTO(BookDTO):
    genres: list["GenreDTO"]


class BookAuthorDTO(BookDTO):
    authors: list["AuthorDTO"]


class BookCatalogDTO(BookDTO):
    catalogs: list["CatalogDTO"]


class BookEditionDTO(BookDTO):
    editions: list["EditionDTO"]


class BookRelDTOFull(BookDTO):
    genres: list["GenreDTO"]
    authors: list["AuthorDTO"]
    catalogs: list["CatalogDTO"]
    editions: list["EditionDTO"]
    country: "CountryDTO"


class BookRelDTO(BookDTO):
    genres: list["GenreDTO"]
    authors: list["AuthorDTO"]
    catalogs: list["CatalogDTO"]
    country: "CountryDTO"


class PublisherAddDTO(BaseModel):
    name: str


class PublisherDTO(PublisherAddDTO):
    id: int


class EditionAddDTO(BaseModel):
    publisher_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    isbn_number: str = Field(max_length=18, default="978-3-16-148410-0")
    page_amount: int = Field(gt=0)
    status: Status
    published_year: int = Field(gt=0, le=2024)
    language_id: int = Field(gt=0)
    instances_available: int = Field(ge=1)

    @field_validator("isbn_number")
    def check_isbn_format(cls, value):
        if value is None:
            return value
        isbn_13_regex = r"^97[89]-\d{1,5}-\d{1,7}-\d{1,6}-\d$"
        if not re.match(isbn_13_regex, value):
            raise ValidationError("Невалидный номер ISBN")
        return value


class EditionDTO(EditionAddDTO):
    id: int = Field(gt=0)


class EditionRelDTO(EditionDTO):
    book: "BookRelDTO"
    publisher: "PublisherDTO"
    language: "LanguageDTO"

    class Config:
        orm_mode = True


class EditionUpdateDTO(EditionAddDTO):
    publisher_id: int | None = Field(gt=0)
    book_id: int | None = Field(gt=0)
    isbn_number: str | None = Field(max_length=18, default="978-3-16-148410-0")
    page_amount: int | None = Field(gt=0)
    status: Status
    published_year: int | None = Field(gt=0, le=2024)
    language_id: int | None = Field(gt=0)
    instances_available: int | None = Field(ge=1)
