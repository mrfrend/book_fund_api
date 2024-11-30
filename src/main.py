from fastapi import FastAPI
from database.database import Base, engine
from database.models import *
import uvicorn
import asyncio
from routers import routers
from repositories.user_repository import UserRepository


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all(engine))
        await conn.run_sync(Base.metadata.create_all(engine))


app = FastAPI(title="Book fund API", summary="API библиотечного фонда")
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
