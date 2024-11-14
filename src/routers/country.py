from fastapi import APIRouter, Depends, HTTPException
from repositories.country_repository import CountryRepository
from schemas.books import CountryDTO, CountryAddDTO
from dependacies import get_country_repository
from typing import Annotated

router = APIRouter(prefix="/countries", tags=["Страны, Countries"])
country_dependency = Annotated[CountryRepository, Depends(get_country_repository)]


@router.get("/", summary="Получить все страны")
def get_all_countrys(repo: country_dependency) -> list[CountryDTO]:
    return repo.get_all()


@router.get("/{country_id}", summary="Получить страну по id")
def get_country(country_id: int, repo: country_dependency) -> CountryDTO | None:
    country = repo.get(id=country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Страна не была найдена")
    return country


@router.post("/", summary="Добавить страну")
def add_country(country: CountryAddDTO, repo: country_dependency) -> CountryDTO:
    country = repo.create(country)
    return country


@router.delete("/{country_id}", summary="Удалить страну по id")
def delete_country(country_id: int, repo: country_dependency):
    res = repo.delete(id=country_id)
    if res:
        return {"message": "Страна удалена"}
    else:
        raise HTTPException(status_code=404, detail="Страна не была найдена")


@router.patch("/{country_id}", summary="Обновить страну по id")
def update_country(
    country_id: int, country: CountryAddDTO, repo: country_dependency
) -> CountryDTO | None:
    country = repo.update(id=country_id, data=country)
    if country is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return country
