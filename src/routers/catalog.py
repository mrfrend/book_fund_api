from fastapi import APIRouter, Depends, HTTPException
from services import CatalogService
from schemas.undepended_schemas import CatalogDTO, CatalogAddDTO
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/catalogs", tags=["Каталоги, Catalogs"])
catalog_dependency = Annotated[CatalogService, Depends(CatalogService)]


@router.get("/", summary="Получить все каталоги")
async def get_all_catalogs(catalog_service: catalog_dependency) -> list[CatalogDTO]:
    return await catalog_service.get_all()


@router.get("/{catalog_id}", summary="Получить каталог по id")
async def get_catalog(catalog_id: int, catalog_service: catalog_dependency) -> CatalogDTO | None:
    catalog = await catalog_service.get(id=catalog_id)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog


@router.post("/", summary="Добавить каталог")
async def add_catalog(catalog: CatalogAddDTO, catalog_service: catalog_dependency, staff_user=Depends(get_staff_user)) -> CatalogDTO:
    catalog = await catalog_service.create(catalog)
    return catalog


@router.delete("/{catalog_id}", summary="Удалить каталог по id")
async def delete_catalog(catalog_id: int, catalog_service: catalog_dependency, staff_user=Depends(get_staff_user)):
    res = await catalog_service.delete(id=catalog_id)
    if res:
        return {"message": "Каталог удален"}
    else:
        raise HTTPException(status_code=404, detail="Каталог не был найден")


@router.patch("/{catalog_id}", summary="Обновить каталог по id")
async def update_catalog(
    catalog_id: int, catalog: CatalogAddDTO, catalog_service: catalog_dependency, staff_user=Depends(get_staff_user)
) -> CatalogDTO | None:
    catalog = await catalog_service.update(id=catalog_id, data=catalog)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog
