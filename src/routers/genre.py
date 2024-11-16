from fastapi import APIRouter, Depends, HTTPException
from services import GenreService
from schemas.schemas import GenreDTO, GenreAddDTO, BookDTO
from dependacies import get_genre_service
from typing import Annotated

router = APIRouter(prefix="/genres", tags=["Жанры, Genres"])
genre_dependency = Annotated[GenreService, Depends(get_genre_service)]


@router.get("/", summary="Получить все жанры")
def get_all_genres(genre_service: genre_dependency) -> list[GenreDTO]:
    return genre_service.get_all()


@router.get("/{genre_id}", summary="Получить жанр по id")
def get_genre(genre_id: int, genre_service: genre_dependency) -> GenreDTO | None:
    genre = genre_service.get(id=genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre


@router.get("/books/{genre_id}", summary="Получить книги по жанру")
def get_books_by_genre(
    genre_id: int, genre_service: genre_dependency
) -> list[BookDTO]:
    books = genre_service.get_books_by_genre_id(genre_id=genre_id)
    return books


@router.post("/", summary="Добавить жанр")
def add_genre(genre: GenreAddDTO, genre_service: genre_dependency) -> GenreDTO:
    genre = genre_service.create(genre)
    return genre


@router.delete("/{genre_id}", summary="Удалить жанр по id")
def delete_genre(genre_id: int, genre_service: genre_dependency):
    res = genre_service.delete(id=genre_id)
    if res:
        return {"message": "Жанр удален"}
    else:
        raise HTTPException(status_code=404, detail="Жанр не был найден")


@router.patch("/{genre_id}", summary="Обновить жанр по id")
def update_genre(
    genre_id: int, genre: GenreAddDTO, genre_service: genre_dependency
) -> GenreDTO | None:
    genre = genre_service.update(id=genre_id, data=genre)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre
