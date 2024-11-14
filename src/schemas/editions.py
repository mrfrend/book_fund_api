from pydantic import BaseModel, Field, field_validator, ValidationError
from database.models import Status
import re


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


class EditionUpdateDTO(EditionAddDTO):
    publisher_id: int | None = Field(gt=0)
    book_id: int | None = Field(gt=0)
    isbn_number: str | None = Field(max_length=18, default="978-3-16-148410-0")
    page_amount: int | None = Field(gt=0)
    status: Status
    published_year: int | None = Field(gt=0, le=2024)
    language_id: int | None = Field(gt=0)
    instances_available: int | None = Field(ge=1)
