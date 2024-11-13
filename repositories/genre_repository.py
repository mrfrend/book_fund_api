from schemas.books import *
from sqlalchemy import select
from database.models import Genre
from schemas.books import GenreDTO, GenreAddDTO
from database.database import session_factory


class GenreRepository:
    @classmethod
    def get_genres(cls) -> list[GenreDTO]:
        with session_factory() as session:
            query = select(Genre)
            res = session.execute(query).scalars().all()
            countries_dto = [
                GenreDTO.model_validate(genre, from_attributes=True)
                for genre in res
            ]
            return countries_dto

    @classmethod
    def get_genre(cls, genre_id: int) -> GenreDTO | None:
        with session_factory() as session:
            genre = session.get(Genre, genre_id)
            if genre is None:
                return None
            return GenreDTO.model_validate(genre, from_attributes=True)

    @classmethod
    def add_genre(cls, data: GenreAddDTO) -> int:
        with session_factory() as session:
            genre_dict = data.model_dump()
            genre = Genre(**genre_dict)
            session.add(genre)
            session.commit()
            session.refresh(genre)
            return genre.id

    @classmethod
    def delete_genre(cls, genre_id: int) -> 0 | 1:
        with session_factory() as session:
            query = select(Genre).where(Genre.id == genre_id)
            genre = session.execute(query).scalar_one_or_none()
            if genre:
                session.delete(genre)
                session.commit()
                return 1
            return 0
