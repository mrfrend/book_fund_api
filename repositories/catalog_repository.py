from schemas.books import *
from sqlalchemy import select
from database.models import Catalog
from schemas.books import CatalogDTO, CatalogAddDTO
from database.database import session_factory


class CatalogRepository:
    @classmethod
    def get_catalogs(cls) -> list[CatalogDTO]:
        with session_factory() as session:
            query = select(Catalog)
            res = session.execute(query).scalars().all()
            countries_dto = [
                CatalogDTO.model_validate(catalog, from_attributes=True)
                for catalog in res
            ]
            return countries_dto

    @classmethod
    def get_catalog(cls, catalog_id: int) -> CatalogDTO | None:
        with session_factory() as session:
            catalog = session.get(Catalog, catalog_id)
            if catalog is None:
                return None
            return CatalogDTO.model_validate(catalog, from_attributes=True)

    @classmethod
    def update_catalog(cls, catalog_id: int, catalog_name: str) -> None | CatalogDTO:
        with session_factory() as session:
            catalog = session.get(Catalog, catalog_id)
            if catalog is None:
                return 0
            catalog.name = catalog_name
            session.commit()
            session.refresh(catalog)
            return catalog

    @classmethod
    def add_catalog(cls, data: CatalogAddDTO) -> int:
        with session_factory() as session:
            catalog_dict = data.model_dump()
            catalog = Catalog(**catalog_dict)
            session.add(catalog)
            session.commit()
            session.refresh(catalog)
            return catalog.id

    @classmethod
    def delete_catalog(cls, catalog_id: int) -> 0 | 1:
        with session_factory() as session:
            query = select(Catalog).where(Catalog.id == catalog_id)
            catalog = session.execute(query).scalar_one_or_none()
            if catalog:
                session.delete(catalog)
                session.commit()
                return 1
            return 0
