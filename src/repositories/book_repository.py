from schemas.books import *
from sqlalchemy import insert
from database.models import Book, BookGenre, Genre
from schemas.books import BookDTO, BookAddDTO, BookUpdateDTO
from database.database import session_factory
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self):
        super().__init__(
            model=Book,
            db_session=session_factory,
        )

    def add_genre(self, book_id: int, genres_id: list[int]):
        with self.db_session() as session:
            book: Book | None = session.get(Book, book_id)
            genres = list(
                filter(
                    lambda x: x is not None,
                    [session.get(Genre, genre_id) for genre_id in genres_id],
                )
            )
            if book is None:
                return None
            book.genres.extend(genres)
            session.commit()
            session.refresh(book)
            return book
