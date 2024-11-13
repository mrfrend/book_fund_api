from pydantic import BaseModel, Field


class PublisherAddDTO(BaseModel):
    name: str


class PublisherDTO(PublisherAddDTO):
    id: int

