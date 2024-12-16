from schemas.undepended_schemas import *
from sqlalchemy import select
from database.models import Catalog
from database.database import async_session_factory
from .base_repository import BaseRepository


class CatalogRepository(BaseRepository[Catalog]):
    def __init__(self):
        super().__init__(
            model=Catalog,
            db_session=async_session_factory,
        )

    async def get_specific_catalogs(self, catalogs: list[str] | None) -> list[Catalog] | None:
        if catalogs is None:
            return None
        catalogs = [int(catalog_id) for catalog_id in catalogs]
        async with self.db_session() as session:
            query = select(Catalog).where(Catalog.id.in_(catalogs))
            result = (await session.execute(query)).scalars().all()
            return result
