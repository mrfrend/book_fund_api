from __future__ import annotations
from pydantic import BaseModel, Field
import enum

__all__ = [
    "GenreAddDTO",
    "GenreDTO",
    "AuthorAddDTO",
    "AuthorUpdateDTO",
    "AuthorDTO",
    "CatalogAddDTO",
    "CatalogDTO",
    "CountryAddDTO",
    "CountryDTO",
    "PublisherAddDTO",
    "PublisherDTO",
]


class GenreAddDTO(BaseModel):
    name: str = Field(max_length=30)


class GenreDTO(GenreAddDTO):
    id: int


class AuthorAddDTO(BaseModel):
    first_name: str = Field(max_length=25, default="Иван")
    last_name: str = Field(max_length=50, default="Иванов")
    middle_name: str | None = Field(max_length=50, default=None)


class AuthorUpdateDTO(BaseModel):
    first_name: str | None = Field(max_length=25, default=None)
    last_name: str | None = Field(max_length=50, default=None)
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


class PublisherAddDTO(BaseModel):
    name: str = Field(max_length=50)


class PublisherDTO(PublisherAddDTO):
    id: int
