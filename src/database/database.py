from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
engine = create_engine(url=settings.db_url, echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self) -> str:
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or i < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"