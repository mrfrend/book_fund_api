from schemas.schemas import *
from database.models import Language
from database.database import session_factory
from .base_repository import BaseRepository


class LanguageRepository(BaseRepository[Language]):
    def __init__(self):
        super().__init__(model=Language, db_session=session_factory)
