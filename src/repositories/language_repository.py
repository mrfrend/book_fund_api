from schemas.undepended_schemas import *
from database.models import Language
from database.database import async_session_factory
from .base_repository import BaseRepository


class LanguageRepository(BaseRepository[Language]):
    def __init__(self):
        super().__init__(model=Language, db_session=async_session_factory)
