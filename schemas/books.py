from pydantic import BaseModel

class LanguageAddDTO(BaseModel):
    name: str


class LanguageDTO(LanguageAddDTO):
    id: int


class GenreAddDTO(BaseModel):
    name: str


class GenreDTO(GenreAddDTO):
    id: int


class AuthorAddDTO(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None


class AuthorDTO(AuthorAddDTO):
    id: int


class CatalogAddDTO(BaseModel):
    name: str


class CatalogDTO(CatalogAddDTO):
    id: int


class CountryAddDTO(BaseModel):
    name: str


class CountryDTO(CountryAddDTO):
    id: int


class BookAddDTO(BaseModel):
    name: str
    title: str
    keywords: str | None = None
    year_released: int
    country_id: int
    description: str


class BookDTO(BookAddDTO):
    id: int
