from fastapi import APIRouter, Depends, HTTPException, Path
from services import BookService
from schemas.books import BookDTO, BookAddDTO, BookUpdateDTO, GenreAddDTO
from dependacies import get_book_service
from typing import Annotated

router = APIRouter(prefix="/books", tags=["Книги, Books"])
book_dependency = Annotated[BookService, Depends(get_book_service)]


@router.get("/", summary="Получить все книги")
def get_all_books(book_service: book_dependency) -> list[BookDTO]:
    return book_service.get_all()


@router.get("/{book_id}", summary="Получить книгу по id")
def get_book(book_id: int, book_service: book_dependency) -> BookDTO | None:
    book = book_service.get(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найдена")
    return book


@router.post("/", summary="Добавить книгу")
def add_book(book: BookAddDTO, book_service: book_dependency) -> BookAddDTO:
    book = book_service.create(book)
    return book


@router.post("/{book_id}", summary="Добавить книге жанр/жанры")
def add_genre_to_book(
    book_id: Annotated[int, Path(gt=0)], genres_id: list[int], book_service: book_dependency
):
    pass


@router.delete("/{book_id}", summary="Удалить книгу по id")
def delete_book(book_id: int, book_service: book_dependency):
    res = book_service.delete(id=book_id)
    if res:
        return {"message": "Книга была удалена"}
    else:
        raise HTTPException(status_code=404, detail="Книга не была найдена")


@router.patch("/{book_id}", summary="Обновить книгу по id")
def update_book(
    book_id: int, book: BookUpdateDTO, book_service: book_dependency
) -> BookDTO | None:
    book = book_service.update(id=book_id, data=book)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найден")
    return book
