from schemas.books import LanguageDTO
from sqlalchemy import select
from database.models import *
from database.database import session_factory


class LanguageRepository:
    @classmethod
    def add_language(cls, language_name: str) -> LanguageDTO:
        with session_factory() as session:
            language = Language(name=language_name)
            session.add(language)
            session.commit()
            session.refresh(language)
            return LanguageDTO.model_validate(language, from_attributes=True)

    @classmethod
    def get_language(cls, language_id: int) -> LanguageDTO:
        with session_factory() as session:
            res = session.get(Language, language_id)
            return LanguageDTO.model_validate(res, from_attributes=True)

    @classmethod
    def update_language(cls, language_id: int, language_name: str) -> None | LanguageDTO:
        with session_factory() as session:
            language = session.get(Language, language_id)
            if language is None:
                return 0
            language.name = language_name
            session.commit()
            session.refresh(language)
            return language

    @classmethod
    def get_languages(cls) -> list[LanguageDTO]:
        with session_factory() as session:
            query = select(Language)
            res = session.execute(query).scalars().all()
            return [
                LanguageDTO.model_validate(row, from_attributes=True) for row in res
            ]

    @classmethod
    def delete_language(cls, language_id: int):
        with session_factory() as session:
            language = session.get(Language, language_id)
            session.delete(language)
            session.commit()

    @classmethod
    def delete_languages(cls):
        with session_factory() as session:
            session.query(Language).delete()
            session.commit()
