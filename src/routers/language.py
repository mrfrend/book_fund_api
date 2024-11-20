from fastapi import APIRouter, Depends, HTTPException
from services import LanguageService
from schemas.schemas import LanguageDTO, LanguageAddDTO
from services.dependacies import get_language_service
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/languages", tags=["Языки, Languages"])
language_dependency = Annotated[LanguageService, Depends(get_language_service)]


@router.get("/", summary="Получить все языки, на которых написаны книги")
def get_all_languages(language_service: language_dependency) -> list[LanguageDTO]:
    return language_service.get_all()


@router.get("/{language_id}", summary="Получить язык по id")
def get_language(
    language_id: int, language_service: language_dependency
) -> LanguageDTO | None:
    language = language_service.get(id=language_id)
    if language is None:
        raise HTTPException(status_code=404, detail="Язык не был найден")
    return language


@router.post("/", summary="Добавить язык")
def add_language(
    language: LanguageAddDTO,
    language_service: language_dependency,
    staff_user=Depends(get_staff_user),
) -> LanguageDTO:
    language = language_service.create(language)
    return language


@router.delete("/{language_id}", summary="Удалить язык по id")
def delete_language(
    language_id: int,
    language_service: language_dependency,
    staff_user=Depends(get_staff_user),
):
    res = language_service.delete(id=language_id)
    if res:
        return {"message": "Язык удален"}
    else:
        raise HTTPException(status_code=404, detail="Язык не был найден")


@router.patch("/{language_id}", summary="Обновить язык по id")
def update_language(
    language_id: int,
    language: LanguageAddDTO,
    language_service: language_dependency,
    staff_user=Depends(get_staff_user),
) -> LanguageDTO | None:
    language = language_service.update(id=language_id, data=language)
    if language is None:
        raise HTTPException(status_code=404, detail="Язык не был найден")
    return language
