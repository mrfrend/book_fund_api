from pydantic import BaseModel, Field


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
    year_realised: int = Field(gt=0, le=2024)
    description: str = Field(max_length=500)
    country_id: int = Field(gt=0)


class BookUpdateDTO(BaseModel):
    title: str | None = Field(max_length=40, default=None)
    keywords: str | None = None
    year_realised: int | None = Field(gt=0, le=2024, default=None)
    description: str | None = Field(max_length=500, default=None)
    country_id: int | None = Field(gt=0, default=None)


class BookDTO(BookAddDTO):
    id: int
