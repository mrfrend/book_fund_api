from sqlalchemy.orm import Session
from schemas.books import *
from sqlalchemy import select
from database.models import Catalog
from schemas.books import CatalogDTO, CatalogAddDTO
from database.database import session_factory
from .base_repository import BaseRepository


class CatalogRepository(BaseRepository[Catalog]):
    def __init__(self):
        super().__init__(
            model=Catalog,
            db_session=session_factory,
        )
