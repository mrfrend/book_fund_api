from schemas.books import *
from database.models import Book
from schemas.books import BookDTO, BookAddDTO, BookUpdateDTO
from database.database import session_factory
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book, BookAddDTO, BookUpdateDTO, BookDTO]):
    def __init__(self):
        super().__init__(
            model=Book,
            db_session=session_factory,
            return_dto=BookDTO,
            create_dto=BookAddDTO,
            update_dto=BookUpdateDTO,
        )
