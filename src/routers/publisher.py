from fastapi import APIRouter, Depends, HTTPException
from repositories.publisher_repository import PublisherRepository
from schemas.editions import PublisherDTO, PublisherAddDTO
from dependacies import get_publisher_repository
from typing import Annotated

router = APIRouter(prefix="/publishers", tags=["Издатели, Publishers"])
publisher_dependency = Annotated[PublisherRepository, Depends(get_publisher_repository)]


@router.get("/", summary="Получить всех издателей")
def get_all_publishers(repo: publisher_dependency) -> list[PublisherDTO]:
    return repo.get_all()


@router.get("/{publisher_id}", summary="Получить издателя по id")
def get_publisher(publisher_id: int, repo: publisher_dependency) -> PublisherDTO | None:
    publisher = repo.get(id=publisher_id)
    if publisher is None:
        raise HTTPException(status_code=404, detail="Издатель не был найден")
    return publisher


@router.post("/", summary="Добавить издателя")
def add_publisher(publisher: PublisherAddDTO, repo: publisher_dependency) -> PublisherDTO:
    publisher = repo.create(publisher)
    return publisher


@router.delete("/{publisher_id}", summary="Удалить издателя по id")
def delete_publisher(publisher_id: int, repo: publisher_dependency):
    res = repo.delete(id=publisher_id)
    if res:
        return {"message": "Издатель был удален"}
    else:
        raise HTTPException(status_code=404, detail="Издатель не был найден")


@router.patch("/{publisher_id}", summary="Обновить издателя по id")
def update_publisher(
    publisher_id: int, publisher: PublisherAddDTO, repo: publisher_dependency
) -> PublisherDTO | None:
    publisher = repo.update(id=publisher_id, data=publisher)
    if publisher is None:
        raise HTTPException(status_code=404, detail="Издатель не был найден")
    return publisher
