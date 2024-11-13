from fastapi import APIRouter, HTTPException
from schemas.books import AuthorDTO, AuthorAddDTO
from repositories.author_repository import AuthorRepository

router = APIRouter(prefix="/authors", tags=["Авторы, Author"])


@router.get(
    "/",
    summary="Получить список всех авторов",
    responses={200: {"model": AuthorDTO, "description": "Авторы были получены"}},
)
def get_all_authors() -> list[AuthorDTO]:
    return AuthorRepository.get_authors()


@router.get("/{author_id}", summary="Получить автора по id")
def get_author_by_id(author_id: int) -> AuthorDTO:
    author = AuthorRepository.get_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author


@router.post("/")
def add_author(author: AuthorAddDTO) -> int:
    author_id = AuthorRepository.add_author(author)
    return {"author_id": author_id}


@router.delete("/{author_id}")
def delete_author(author_id: int):
    res = AuthorRepository.delete_author(author_id)
    if not res:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return {"msg": "Автор удален"}
