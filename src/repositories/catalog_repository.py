
from schemas.undepended_schemas import *
from sqlalchemy import select
from database.models import Catalog
from database.database import session_factory
from .base_repository import BaseRepository


class CatalogRepository(BaseRepository[Catalog]):
    def __init__(self):
        super().__init__(
            model=Catalog,
            db_session=session_factory,
        )

    def get_specific_catalogs(self, catalogs: list[str]) -> list[Catalog]:
        with self.db_session() as session:
            query = select(Catalog).where(Catalog.name.in_(catalogs))
            result = session.execute(query).scalars().all()
            return result