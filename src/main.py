from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base, sync_engine
from database.models import *
import uvicorn
from routers import routers

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]


def create_tables():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


app = FastAPI(title="Book fund API", summary="API библиотечного фонда")
for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
