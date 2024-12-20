from schemas.undepended_schemas import *
from database.models import Country
from database.database import async_session_factory
from .base_repository import BaseRepository


class CountryRepository(BaseRepository[Country]):
    def __init__(self):
        super().__init__(
            model=Country,
            db_session=async_session_factory,
        )
