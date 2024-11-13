from repositories.base_repository import BaseRepository
from database.models import Publisher
from schemas.editions import PublisherDTO, PublisherAddDTO
from repositories.base_repository import BaseRepository
from database.database import session_factory


class PublisherRepository(
    BaseRepository[Publisher, PublisherAddDTO, PublisherAddDTO, PublisherDTO]
):
    def __init__(self):
        super().__init__(
            model=Publisher,
            db_session=session_factory,
            return_dto=PublisherDTO,
            create_dto=PublisherAddDTO,
            update_dto=PublisherAddDTO,
        )
