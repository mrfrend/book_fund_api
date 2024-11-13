from fastapi import APIRouter, Depends, HTTPException
from repositories.genre_repository import GenreRepository
from schemas.books import GenreDTO, GenreAddDTO
from dependacies import get_genre_repository
from typing import Annotated

router = APIRouter(prefix="/genres", tags=["Жанры, Genres"])
genre_dependency = Annotated[GenreRepository, Depends(get_genre_repository)]


@router.get("/", summary="Получить все жанры")
def get_all_genres(repo: genre_dependency) -> list[GenreDTO]:
    return repo.get_all()


@router.get("/{genre_id}", summary="Получить жанр по id")
def get_genre(genre_id: int, repo: genre_dependency) -> GenreDTO | None:
    genre = repo.get(id=genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre


@router.post("/", summary="Добавить жанр")
def add_genre(genre: GenreAddDTO, repo: genre_dependency) -> GenreDTO:
    genre = repo.create(genre)
    return genre


@router.delete("/{genre_id}", summary="Удалить жанр по id")
def delete_genre(genre_id: int, repo: genre_dependency):
    res = repo.delete(id=genre_id)
    if res:
        return {"message": "Жанр удален"}
    else:
        raise HTTPException(status_code=404, detail="Жанр не был найден")


@router.patch("/{genre_id}", summary="Обновить жанр по id")
def update_genre(
    genre_id: int, genre: GenreAddDTO, repo: genre_dependency
) -> GenreDTO | None:
    genre = repo.update(id=genre_id, data=genre)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre
