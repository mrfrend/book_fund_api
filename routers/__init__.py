from .language import router as language_router
from .author import router as author_router
from .country import router as country_router
from .genre import router as genre_router

routers = [language_router, author_router, country_router, genre_router]
