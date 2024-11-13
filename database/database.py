from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///book_fund.db", echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
