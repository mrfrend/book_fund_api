from fastapi import APIRouter, Depends, HTTPException
from services import GenreService
from schemas import GenreDTO, GenreAddDTO, BookDTO
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/genres", tags=["Жанры, Genres"])
genre_dependency = Annotated[GenreService, Depends(GenreService)]


@router.get("/", summary="Получить все жанры")
async def get_all_genres(genre_service: genre_dependency) -> list[GenreDTO]:
    return await genre_service.get_all()


@router.get("/{genre_id}", summary="Получить жанр по id")
async def get_genre(genre_id: int, genre_service: genre_dependency) -> GenreDTO | None:
    genre = await genre_service.get(id=genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre


@router.get("/books/{genre_id}", summary="Получить книги по жанру")
async def get_books_by_genre(genre_id: int, genre_service: genre_dependency) -> list[BookDTO]:
    books = await genre_service.get_books_by_genre_id(genre_id=genre_id)
    return books


@router.post("/", summary="Добавить жанр")
async def add_genre(
    genre: GenreAddDTO,
    genre_service: genre_dependency,
    staff_user=Depends(get_staff_user),
) -> GenreDTO:
    genre = await genre_service.create(genre)
    return genre


@router.delete("/{genre_id}", summary="Удалить жанр по id")
async def delete_genre(
    genre_id: int, genre_service: genre_dependency, staff_user=Depends(get_staff_user)
):
    res = await genre_service.delete(id=genre_id)
    if res:
        return {"message": "Жанр удален"}
    else:
        raise HTTPException(status_code=404, detail="Жанр не был найден")


@router.patch("/{genre_id}", summary="Обновить жанр по id")
async def update_genre(
    genre_id: int,
    genre: GenreAddDTO,
    genre_service: genre_dependency,
    staff_user=Depends(get_staff_user),
) -> GenreDTO | None:
    genre = await genre_service.update(id=genre_id, data=genre)
    if genre is None:
        raise HTTPException(status_code=404, detail="Жанр не был найден")
    return genre
