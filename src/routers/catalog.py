from fastapi import APIRouter, Depends, HTTPException
from services import CatalogService
from schemas.books import CatalogDTO, CatalogAddDTO
from dependacies import get_catalog_service
from typing import Annotated

router = APIRouter(prefix="/catalogs", tags=["Каталоги, Catalogs"])
catalog_dependency = Annotated[CatalogService, Depends(get_catalog_service)]


@router.get("/", summary="Получить все каталоги")
def get_all_catalogs(catalog_service: catalog_dependency) -> list[CatalogDTO]:
    return catalog_service.get_all()


@router.get("/{catalog_id}", summary="Получить каталог по id")
def get_catalog(catalog_id: int, catalog_service: catalog_dependency) -> CatalogDTO | None:
    catalog = catalog_service.get(id=catalog_id)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog


@router.post("/", summary="Добавить каталог")
def add_catalog(catalog: CatalogAddDTO, catalog_service: catalog_dependency) -> CatalogDTO:
    catalog = catalog_service.create(catalog)
    return catalog


@router.delete("/{catalog_id}", summary="Удалить каталог по id")
def delete_catalog(catalog_id: int, catalog_service: catalog_dependency):
    res = catalog_service.delete(id=catalog_id)
    if res:
        return {"message": "Каталог удален"}
    else:
        raise HTTPException(status_code=404, detail="Каталог не был найден")


@router.patch("/{catalog_id}", summary="Обновить каталог по id")
def update_catalog(
    catalog_id: int, catalog: CatalogAddDTO, catalog_service: catalog_dependency
) -> CatalogDTO | None:
    catalog = catalog_service.update(id=catalog_id, data=catalog)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog
