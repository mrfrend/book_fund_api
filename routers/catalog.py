from fastapi import APIRouter, Depends, HTTPException
from repositories.catalog_repository import CatalogRepository
from schemas.books import CatalogDTO, CatalogAddDTO
from dependacies import get_catalog_repository
from typing import Annotated

router = APIRouter(prefix="/catalogs", tags=["Каталоги, Catalogs"])
catalog_dependency = Annotated[CatalogRepository, Depends(get_catalog_repository)]


@router.get("/", summary="Получить все каталоги")
def get_all_catalogs(repo: catalog_dependency) -> list[CatalogDTO]:
    return repo.get_all()


@router.get("/{catalog_id}", summary="Получить каталог по id")
def get_catalog(catalog_id: int, repo: catalog_dependency) -> CatalogDTO | None:
    catalog = repo.get(id=catalog_id)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog


@router.post("/", summary="Добавить каталог")
def add_catalog(catalog: CatalogAddDTO, repo: catalog_dependency) -> CatalogDTO:
    catalog = repo.create(catalog)
    return catalog


@router.delete("/{catalog_id}", summary="Удалить каталог по id")
def delete_catalog(catalog_id: int, repo: catalog_dependency):
    res = repo.delete(id=catalog_id)
    if res:
        return {"message": "Каталог удален"}
    else:
        raise HTTPException(status_code=404, detail="Каталог не был найден")


@router.patch("/{catalog_id}", summary="Обновить каталог по id")
def update_catalog(
    catalog_id: int, catalog: CatalogAddDTO, repo: catalog_dependency
) -> CatalogDTO | None:
    catalog = repo.update(id=catalog_id, data=catalog)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Каталог не был найден")
    return catalog
