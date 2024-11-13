from fastapi import APIRouter, Depends, HTTPException
from repositories.author_repository import AuthorRepository
from schemas.books import AuthorDTO, AuthorAddDTO, AuthorUpdateDTO
from dependacies import get_author_repository
from typing import Annotated

router = APIRouter(prefix="/authors", tags=["Авторы, Authors"])
author_dependency = Annotated[AuthorRepository, Depends(get_author_repository)]


@router.get("/", summary="Получить всех авторов")
def get_all_authors(repo: author_dependency) -> list[AuthorDTO]:
    return repo.get_all()


@router.get("/{author_id}", summary="Получить автора по id")
def get_author(author_id: int, repo: author_dependency) -> AuthorDTO | None:
    author = repo.get(id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не был найден")
    return author


@router.post("/", summary="Добавить автора")
def add_author(author: AuthorAddDTO, repo: author_dependency) -> AuthorDTO:
    author = repo.create(author)
    return author


@router.delete("/{author_id}", summary='Удалить автора по id')
def delete_author(author_id: int, repo: author_dependency):
    res = repo.delete(id=author_id)
    if res:
        return {"message": "Автор удален"}
    else:
        raise HTTPException(status_code=404, detail="Автор не был найден")


@router.patch("/{author_id}", summary='Обновить автора по id')
def update_author(
    author_id: int, author: AuthorUpdateDTO, repo: author_dependency
) -> AuthorDTO | None:
    author = repo.update(id=author_id, data=author)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не был найден")
    return author
