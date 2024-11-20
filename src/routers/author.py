from fastapi import APIRouter, Depends, HTTPException
from services import AuthorService
from schemas import AuthorDTO, AuthorAddDTO, AuthorUpdateDTO, BookDTO
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/authors", tags=["Авторы, Authors"])
author_dependency = Annotated[AuthorService, Depends(AuthorService)]


@router.get("/", summary="Получить всех авторов")
def get_all_authors(author_service: author_dependency) -> list[AuthorDTO]:
    return author_service.get_all()


@router.get(
    "/books/{author_id}",
    summary="Получить книги, написанные автором",
    response_model=list[BookDTO],
)
def get_books_by_author(author_id: int, author_service: author_dependency):
    books = author_service.get_books_by_author_id(author_id=author_id)
    return books


@router.get("/{author_id}", summary="Получить автора по id")
def get_author(author_id: int, author_service: author_dependency) -> AuthorDTO | None:
    author = author_service.get(id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не был найден")
    return author


@router.post("/", summary="Добавить автора")
def add_author(
    author: AuthorAddDTO,
    author_service: author_dependency,
    staff_user=Depends(get_staff_user),
) -> AuthorDTO:
    author = author_service.create(author)
    return author


@router.delete("/{author_id}", summary="Удалить автора по id")
def delete_author(
    author_id: int,
    author_service: author_dependency,
    staff_user=Depends(get_staff_user),
):
    res = author_service.delete(id=author_id)
    if res:
        return {"message": "Автор удален"}
    else:
        raise HTTPException(status_code=404, detail="Автор не был найден")


@router.patch("/{author_id}", summary="Обновить автора по id")
def update_author(
    author_id: int,
    author: AuthorUpdateDTO,
    author_service: author_dependency,
    staff_user=Depends(get_staff_user),
) -> AuthorDTO | None:
    author = author_service.update(id=author_id, data=author)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не был найден")
    return author
