from fastapi import FastAPI
from database.database import Base, engine
from database.models import *
import uvicorn
from routers import routers
from repositories.edition_repository import EditionRepository
from services.services import EditionService


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


app = FastAPI(title="Book fund API", summary="API библиотечного фонда")
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    # print(EditionService().get_all())
    # # EditionRepository().get_all()
    uvicorn.run("main:app", port=8000, reload=True)
