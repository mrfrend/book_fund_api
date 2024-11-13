from schemas.books import *
from database.models import Genre
from schemas.books import GenreDTO, GenreAddDTO
from database.database import session_factory
from .base_repository import BaseRepository


class GenreRepository(BaseRepository[Genre, GenreAddDTO, GenreAddDTO, GenreDTO]):
    def __init__(self):
        super().__init__(
            model=Genre,
            db_session=session_factory,
            return_dto=GenreDTO,
            create_dto=GenreAddDTO,
            update_dto=GenreAddDTO,
        )
