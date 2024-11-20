from repositories.base_repository import BaseRepository
from database.models import Publisher
from repositories.base_repository import BaseRepository
from database.database import session_factory


class PublisherRepository(BaseRepository[Publisher]):
    def __init__(self):
        super().__init__(
            model=Publisher,
            db_session=session_factory,
        )
