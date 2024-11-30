from fastapi import APIRouter, Depends, HTTPException, Path
from services import BookService
from schemas import (
    BookRelDTO,
    BookDTO,
    BookAddDTO,
    BookGenreDTO,
    BookAuthorDTO,
    BookCatalogDTO,
    BookEditionDTO,
    BookUpdateDTO,
)
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/books", tags=["Книги, Books"])
book_dependency = Annotated[BookService, Depends(BookService)]


@router.get("/", summary="Получить все книги")
async def get_all_books(book_service: book_dependency) -> list[BookRelDTO]:
    return await book_service.get_all()


@router.get("/{book_id}", summary="Получить книгу по id")
async def get_book(book_id: int, book_service: book_dependency) -> BookDTO | None:
    book = await book_service.get(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найдена")
    return book


@router.post("/", summary="Добавить книгу")
async def add_book(
    book: BookAddDTO, book_service: book_dependency, staff_user=Depends(get_staff_user)
) -> BookAddDTO:
    book = await book_service.create(book)
    return book


@router.post(
    "/genre/{book_id}",
    summary="Добавить книге жанр/жанры",
    response_model=BookGenreDTO,
)
async def add_genres_to_book(
    book_id: Annotated[int, Path(gt=0)],
    genres: list[str],
    book_service: book_dependency,
    staff_user=Depends(get_staff_user),
):
    updated_book = await book_service.add_genres(book_id=book_id, genres=genres)
    return updated_book


@router.post(
    "/author/{book_id}",
    summary="Добавить книге автора/авторов",
    response_model=BookAuthorDTO,
)
async def add_authors_to_book(
    book_id: Annotated[int, Path(gt=0)],
    authors_id: list[int],
    book_service: book_dependency,
    staff_user=Depends(get_staff_user),
):
    updated_book = await book_service.add_authors(
        book_id=book_id, authors_id=authors_id
    )
    return updated_book


@router.post(
    "/catalog/{book_id}",
    summary="Добавить книгу в каталог/каталоги",
    response_model=BookCatalogDTO,
)
async def add_book_to_catalogs(
    book_id,
    catalogs: list[str],
    book_service: book_dependency,
    staff_user=Depends(get_staff_user),
):
    updated_book = await book_service.add_catalogs(book_id=book_id, catalogs=catalogs)
    return updated_book


@router.post(
    "/edition/{book_id}",
    summary="Добавить книгу в издание/издания",
    response_model=BookEditionDTO,
)
async def add_book_to_editions(
    book_id,
    editions_id: list[int],
    book_service: book_dependency,
    staff_user=Depends(get_staff_user),
):
    updated_book = await book_service.add_editions(
        book_id=book_id, editions_id=editions_id
    )
    return updated_book


@router.delete("/{book_id}", summary="Удалить книгу по id")
async def delete_book(
    book_id: int, book_service: book_dependency, staff_user=Depends(get_staff_user)
):
    res = await book_service.delete(id=book_id)
    if res:
        return {"message": "Книга была удалена"}
    else:
        raise HTTPException(status_code=404, detail="Книга не была найдена")


@router.patch("/{book_id}", summary="Обновить книгу по id")
async def update_book(
    book_id: int,
    book: BookUpdateDTO,
    book_service: book_dependency,
    staff_user=Depends(get_staff_user),
) -> BookDTO | None:
    book = await book_service.update(id=book_id, data=book)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найден")
    return book
