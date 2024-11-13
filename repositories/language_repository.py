from schemas.books import *
from database.models import Language
from schemas.books import LanguageDTO, LanguageAddDTO
from database.database import session_factory
from .base_repository import BaseRepository


class LanguageRepository(
    BaseRepository[Language, LanguageAddDTO, LanguageAddDTO, LanguageDTO]
):
    def __init__(self):
        super().__init__(
            model=Language,
            db_session=session_factory,
            return_dto=LanguageDTO,
            create_dto=LanguageAddDTO,
            update_dto=LanguageAddDTO,
        )
