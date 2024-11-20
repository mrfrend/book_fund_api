from fastapi import APIRouter, Depends, HTTPException
from services import CountryService
from schemas.schemas import CountryDTO, CountryAddDTO
from services.dependacies import get_country_service
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/countries", tags=["Страны, Countries"])
country_dependency = Annotated[CountryService, Depends(get_country_service)]


@router.get("/", summary="Получить все страны")
def get_all_countrys(country_service: country_dependency) -> list[CountryDTO]:
    return country_service.get_all()


@router.get("/{country_id}", summary="Получить страну по id")
def get_country(country_id: int, country_service: country_dependency) -> CountryDTO | None:
    country = country_service.get(id=country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Страна не была найдена")
    return country


@router.post("/", summary="Добавить страну")
def add_country(country: CountryAddDTO, country_service: country_dependency, staff_user=Depends(get_staff_user)) -> CountryDTO:
    country = country_service.create(country)
    return country


@router.delete("/{country_id}", summary="Удалить страну по id")
def delete_country(country_id: int, country_service: country_dependency, staff_user=Depends(get_staff_user)):
    res = country_service.delete(id=country_id)
    if res:
        return {"message": "Страна удалена"}
    else:
        raise HTTPException(status_code=404, detail="Страна не была найдена")


@router.patch("/{country_id}", summary="Обновить страну по id")
def update_country(
    country_id: int, country: CountryAddDTO, country_service: country_dependency, staff_user=Depends(get_staff_user)
) -> CountryDTO | None:
    country = country_service.update(id=country_id, data=country)
    if country is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return country
