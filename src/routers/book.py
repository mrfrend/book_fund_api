from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    Form,
    UploadFile,
    Response,
)
from schemas.book_schemas import BookUpdateFrontDTO
from services import BookService
from repositories import BookRepository
from schemas import (
    BookRelDTO,
    BookDTO,
    BookAddDTO,
    BookGenreDTO,
    BookAuthorDTO,
    BookCatalogDTO,
    BookUpdateDTO,
)
from typing import Annotated
from auth.dependancies import get_current_user

router = APIRouter(prefix="/books", tags=["Книги, Books"])
book_dependency = Annotated[BookService, Depends(BookService)]


@router.get("/", summary="Получить все книги")
async def get_all_books(book_service: book_dependency) -> list[BookRelDTO]:
    return await book_service.get_all()


@router.get("/{book_id}", summary="Получить книгу по id")
async def get_book(book_id: int, book_service: book_dependency) -> BookRelDTO | None:
    book = await book_service.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не была найдена")
    return book


@router.post(
    "/",
    summary="Добавить книгу",
    response_model=BookRelDTO,
    response_model_exclude={"img_path"},
)
async def add_book(
    image: UploadFile,
    book_service: book_dependency,
    title: str = Form(max_length=100),
    year_creation: int = Form(gt=0, le=2024),
    year_published: int = Form(gt=0, le=2024),
    isbn_number: str = Form(
        max_length=18, regex=r"^97[89]-\d{1,5}-\d{1,7}-\d{1,6}-\d$"
    ),
    page_amount: int = Form(gt=0),
    quantity: int = Form(gt=0),
    description: str = Form(max_length=800),
    country_id: int = Form(gt=0),
    publisher_id: int = Form(gt=0),
    authors: list[str] = Form(default=[]),
    genres: list[str] = Form(default=[]),
    catalogs: list[str] = Form(default=[]),
    staff_user=Depends(get_current_user),
):
    book_model = BookAddDTO(
        image=image,
        title=title,
        year_creation=year_creation,
        year_published=year_published,
        page_amount=page_amount,
        quantity=quantity,
        description=description,
        country_id=country_id,
        publisher_id=publisher_id,
        authors=authors,
        genres=genres,
        catalogs=catalogs,
        isbn_number=isbn_number,
    )
    try:
        book = await book_service.create(book_model, image)
        return book
    except Exception as e:
        print("Такая ошибка", e)


@router.get("/image/{book_id}", summary="Получить картинку книги")
async def get_image_book(book_id: int, book_service: book_dependency):
    image_content, image_path = await book_service.get_image_book(book_id)
    return Response(
        content=image_content, media_type=f"image/{image_path.split('.')[-1]}"
    )


@router.post(
    "/genre/{book_id}",
    summary="Добавить книге жанр/жанры",
    response_model=BookGenreDTO,
)
async def add_genres_to_book(
    book_id: Annotated[int, Path(gt=0)],
    genres: list[str],
    book_service: book_dependency,
    staff_user=Depends(get_current_user),
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
    staff_user=Depends(get_current_user),
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
    staff_user=Depends(get_current_user),
):
    updated_book = await book_service.add_catalogs(book_id=book_id, catalogs=catalogs)
    return updated_book


@router.delete("/{book_id}", summary="Удалить книгу по id")
async def delete_book(
    book_id: int, book_service: book_dependency, staff_user=Depends(get_current_user)
):
    res = await book_service.delete(id=book_id)
    if res:
        return {"message": "Книга была удалена"}
    else:
        raise HTTPException(status_code=404, detail="Книга не была найдена")


@router.patch("/{book_id}", summary="Обновить книгу по id")
async def update_book(
    book_id: int,
    book_service: book_dependency,
    title: str | None = Form(default=None),
    year_creation: str | None = Form(gt=0, le=2024, default=None),
    year_published: int | None = Form(gt=0, le=2024, default=None),
    page_amount: int | None = Form(gt=0, default=None),
    quantity: int | None = Form(gt=0, default=None),
    isbn_number: str | None = Form(max_length=18, default=None),
    description: str | None = Form(max_length=800, default=None),
    country_id: int | None = Form(gt=0, default=None),
    publisher_id: int | None = Form(gt=0, default=None),
    image: UploadFile | None = File(default=None),
    staff_user=Depends(get_current_user),
) -> BookRelDTO:
    book_model = BookUpdateFrontDTO(
        title=title,
        year_creation=year_creation,
        year_published=year_published,
        page_amount=page_amount,
        quantity=quantity,
        isbn_number=isbn_number,
        description=description,
        country_id=country_id,
        publisher_id=publisher_id,
    )
    updated_book = await book_service.update(id=book_id, data=book_model, image=image)
    return updated_book


# @router.post(
#     "/edition/{book_id}",
#     summary="Добавить книгу в издание/издания",
#     response_model=BookEditionDTO,
# )
# async def add_book_to_editions(
#     book_id,
#     editions_id: list[int],
#     book_service: book_dependency,
#     staff_user=Depends(get_current_user),
# ):
#     updated_book = await book_service.add_editions(
#         book_id=book_id, editions_id=editions_id
#     )
#     return updated_book
