from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
engine = create_engine(url=settings.db_url, echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
