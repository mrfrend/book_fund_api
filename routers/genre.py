from fastapi import APIRouter, HTTPException
from schemas.books import GenreDTO, GenreAddDTO
from repositories.genre_repository import GenreRepository

router = APIRouter(prefix="/genres", tags=["Жанры, Genres"])


@router.get(
    "/",
    summary="Получить список всех жанров",
    responses={200: {"model": GenreDTO, "description": "Получить все жанры"}},
)
def get_all_countries() -> list[GenreDTO]:
    return GenreRepository.get_genres()


@router.get("/{genre_id}", summary="Получить жанр по id")
def get_genre_by_id(genre_id: int) -> GenreDTO:
    genre = GenreRepository.get_genre(genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return genre


@router.post("/", summary="Добавить жанр")
def add_genre(genre: GenreAddDTO):
    genre_id = GenreRepository.add_genre(genre)
    return {"genre_id": genre_id}


@router.delete("/{genre_id}")
def delete_genre(genre_id: int):
    res = GenreRepository.delete_genre(genre_id)
    if not res:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return {"msg": "Жанр удален"}
