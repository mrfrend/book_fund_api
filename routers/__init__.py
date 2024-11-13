from .language import router as language_router
from .author import router as author_router
from .country import router as country_router
from .genre import router as genre_router
from .catalog import router as catalog_router
from .publisher import router as publisher_router
from .book import router as book_router

routers = [
    language_router,
    author_router,
    country_router,
    genre_router,
    catalog_router,
    publisher_router,
    book_router,
]
