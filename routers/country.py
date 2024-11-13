from fastapi import APIRouter, HTTPException
from schemas.books import CountryDTO, CountryAddDTO
from repositories.country_repository import CountryRepository

router = APIRouter(prefix="/countries", tags=["Страны, Countries"])


@router.get(
    "/",
    summary="Получить список всех стран, в которых были написаны книги",
    responses={200: {"model": CountryDTO, "description": "Получить все страны"}},
)
def get_all_countries() -> list[CountryDTO]:
    return CountryRepository.get_countries()


@router.get("/{country_id}", summary="Получить страну по id")
def get_country_by_id(country_id: int) -> CountryDTO:
    country = CountryRepository.get_country(country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return country


@router.post("/", summary="Добавить страну")
def add_country(country: CountryAddDTO):
    country_id = CountryRepository.add_country(country)
    return {"country_id": country_id}


@router.delete("/{country_id}")
def delete_country(country_id: int):
    res = CountryRepository.delete_country(country_id)
    if not res:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return {"msg": "Страна удалена"}
