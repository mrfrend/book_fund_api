from fastapi import APIRouter, HTTPException
from schemas.books import CatalogDTO, CatalogAddDTO
from repositories.catalog_repository import CatalogRepository

router = APIRouter(prefix="/catalogs", tags=["Каталоги, Catalogs"])


@router.get(
    "/",
    summary="Получить список всех стран, в которых были написаны книги",
    responses={200: {"model": CatalogDTO, "description": "Получить все страны"}},
)
def get_all_countries() -> list[CatalogDTO]:
    return CatalogRepository.get_countries()


@router.get("/{catalog_id}", summary="Получить страну по id")
def get_catalog_by_id(catalog_id: int) -> CatalogDTO:
    catalog = CatalogRepository.get_catalog(catalog_id)
    if catalog is None:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return catalog


@router.post("/", summary="Добавить страну")
def add_catalog(catalog: CatalogAddDTO):
    catalog_id = CatalogRepository.add_catalog(catalog)
    return {"catalog_id": catalog_id}


@router.delete("/{catalog_id}")
def delete_catalog(catalog_id: int):
    res = CatalogRepository.delete_catalog(catalog_id)
    if not res:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    return {"msg": "Страна удалена"}
