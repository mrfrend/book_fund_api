from fastapi import APIRouter, Depends, HTTPException
from repositories.book_repository import BookRepository
from schemas.books import BookDTO, BookAddDTO, BookUpdateDTO
from dependacies import get_book_repository
from typing import Annotated

router = APIRouter(prefix="/books", tags=["Книги, Books"])
book_dependency = Annotated[BookRepository, Depends(get_book_repository)]


@router.get("/", summary="Получить все книги")
def get_all_books(repo: book_dependency) -> list[BookDTO]:
    return repo.get_all()


@router.get("/{book_id}", summary="Получить книгу по id")
def get_book(book_id: int, repo: book_dependency) -> BookDTO | None:
    book = repo.get(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найдена")
    return book


@router.post("/", summary="Добавить книгу")
def add_book(book: BookAddDTO, repo: book_dependency) -> BookDTO:
    book = repo.create(book)
    return book


@router.delete("/{book_id}", summary="Удалить книгу по id")
def delete_book(book_id: int, repo: book_dependency):
    res = repo.delete(id=book_id)
    if res:
        return {"message": "Книга была удалена"}
    else:
        raise HTTPException(status_code=404, detail="Книга не была найдена")


@router.patch("/{book_id}", summary="Обновить книгу по id")
def update_book(
    book_id: int, book: BookUpdateDTO, repo: book_dependency
) -> BookDTO | None:
    book = repo.update(id=book_id, data=book)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найден")
    return book
