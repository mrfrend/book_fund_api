from schemas.books import *
from database.models import Country
from schemas.books import CountryDTO, CountryAddDTO
from database.database import session_factory
from .base_repository import BaseRepository


class CountryRepository(BaseRepository[Country, CountryAddDTO, CountryAddDTO, CountryDTO]):
    def __init__(self):
        super().__init__(
            model=Country,
            db_session=session_factory,
            return_dto=CountryDTO,
            create_dto=CountryAddDTO,
            update_dto=CountryAddDTO
        )
