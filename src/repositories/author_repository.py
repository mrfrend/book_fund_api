from database.models import Author
from schemas.books import AuthorDTO, AuthorAddDTO, AuthorUpdateDTO
from database.database import session_factory
from .base_repository import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(
            model=Author,
            db_session=session_factory,
        )
