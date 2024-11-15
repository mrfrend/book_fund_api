from schemas.books import *
from database.models import Edition
from schemas.editions import EditionDTO, EditionAddDTO, EditionUpdateDTO
from database.database import session_factory
from .base_repository import BaseRepository


class EditionRepository(BaseRepository[Edition]):
    def __init__(self):
        super().__init__(
            model=Edition,
            db_session=session_factory,
        )
