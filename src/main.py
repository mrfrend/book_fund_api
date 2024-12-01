from fastapi import FastAPI
from database.database import Base, sync_engine
from database.models import *
import uvicorn
import asyncio
from routers import routers
from repositories.user_repository import UserRepository


def create_tables():
    Base.metadata.drop_all(bind=sync_engine)
    # Base.metadata.create_all(bind=sync_engine)


app = FastAPI(title="Book fund API", summary="API библиотечного фонда")
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=sync_engine)
    uvicorn.run("main:app", port=8000, reload=True)
