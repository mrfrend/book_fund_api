from fastapi import APIRouter
from repositories.language_repository import LanguageRepository
from schemas.books import *

router = APIRouter(prefix="/languages", tags=["Языки, Languages"])


@router.get("/", response_model=list[LanguageDTO])
def get_all_languages():
    languages = LanguageRepository.get_languages()
    return languages


@router.post("/", response_model=LanguageDTO)
def add_language(language: LanguageAddDTO):
    language = LanguageRepository.add_language(language.name)
    return language


@router.get("/{language_id}", response_model=LanguageDTO)
def get_language_by_id(language_id: int):
    language = LanguageRepository.get_language_by_id(language_id)
    return language


@router.patch("/{language_id}", response_model=LanguageDTO)
def update_language_by_id(language_id: int, language: LanguageAddDTO):
    language = LanguageRepository.update_language(language_id, language.name)
    if language is None:
        raise HTTPException(status_code=404, detail="Язык не найден")
    return language


@router.delete("/{language_id}")
def delete_language_by_id(language_id: int):
    LanguageRepository.delete_language(language_id)
    return {"message": "Язык был удален"}


@router.delete("/")
def delete_languages():
    LanguageRepository.delete_languages()
    return {"message": "Все языки были удалены"}
