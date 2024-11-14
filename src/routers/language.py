from fastapi import APIRouter, Depends, HTTPException
from repositories.language_repository import LanguageRepository
from schemas.books import LanguageDTO, LanguageAddDTO
from dependacies import get_language_repository
from typing import Annotated

router = APIRouter(prefix="/languages", tags=["Языки, Languages"])
language_dependency = Annotated[LanguageRepository, Depends(get_language_repository)]


@router.get("/", summary="Получить все языки, на которых написаны книги")
def get_all_languages(repo: language_dependency) -> list[LanguageDTO]:
    return repo.get_all()


@router.get("/{language_id}", summary="Получить язык по id")
def get_language(language_id: int, repo: language_dependency) -> LanguageDTO | None:
    language = repo.get(id=language_id)
    if language is None:
        raise HTTPException(status_code=404, detail="Язык не был найден")
    return language


@router.post("/", summary="Добавить язык")
def add_language(language: LanguageAddDTO, repo: language_dependency) -> LanguageDTO:
    language = repo.create(language)
    return language


@router.delete("/{language_id}", summary="Удалить язык по id")
def delete_language(language_id: int, repo: language_dependency):
    res = repo.delete(id=language_id)
    if res:
        return {"message": "Язык удален"}
    else:
        raise HTTPException(status_code=404, detail="Язык не был найден")


@router.patch("/{language_id}", summary="Обновить язык по id")
def update_language(
    language_id: int, language: LanguageAddDTO, repo: language_dependency
) -> LanguageDTO | None:
    language = repo.update(id=language_id, data=language)
    if language is None:
        raise HTTPException(status_code=404, detail="Язык не был найден")
    return language
