from database.models import Author
from schemas.books import AuthorDTO, AuthorAddDTO, AuthorUpdateDTO
from database.database import session_factory
from .base_repository import BaseRepository


class AuthorRepository(
    BaseRepository[Author, AuthorAddDTO, AuthorUpdateDTO, AuthorDTO]
):
    def __init__(self):
        super().__init__(
            model=Author,
            db_session=session_factory,
            return_dto=AuthorDTO,
            create_dto=AuthorAddDTO,
            update_dto=AuthorUpdateDTO,
        )
