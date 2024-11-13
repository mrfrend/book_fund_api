from repositories.language_repository import LanguageRepository
from database.database import session_factory


def get_library_repository():
    return LanguageRepository(session_factory)
