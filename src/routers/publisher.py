from fastapi import APIRouter, Depends, HTTPException
from services import PublisherService
from schemas.undepended_schemas import PublisherDTO, PublisherAddDTO
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/publishers", tags=["Издатели, Publishers"])
publisher_dependency = Annotated[PublisherService, Depends(PublisherService)]


@router.get("/", summary="Получить всех издателей")
def get_all_publishers(publisher_service: publisher_dependency) -> list[PublisherDTO]:
    return publisher_service.get_all()


@router.get("/{publisher_id}", summary="Получить издателя по id")
def get_publisher(
    publisher_id: int, publisher_service: publisher_dependency
) -> PublisherDTO | None:
    publisher = publisher_service.get(id=publisher_id)
    if publisher is None:
        raise HTTPException(status_code=404, detail="Издатель не был найден")
    return publisher


@router.post("/", summary="Добавить издателя")
def add_publisher(
    publisher: PublisherAddDTO,
    publisher_service: publisher_dependency,
    staff_user=Depends(get_staff_user),
) -> PublisherDTO:
    publisher = publisher_service.create(publisher)
    return publisher


@router.delete("/{publisher_id}", summary="Удалить издателя по id")
def delete_publisher(
    publisher_id: int,
    publisher_service: publisher_dependency,
    staff_user=Depends(get_staff_user),
):
    res = publisher_service.delete(id=publisher_id)
    if res:
        return {"message": "Издатель был удален"}
    else:
        raise HTTPException(status_code=404, detail="Издатель не был найден")


@router.patch("/{publisher_id}", summary="Обновить издателя по id")
def update_publisher(
    publisher_id: int,
    publisher: PublisherAddDTO,
    publisher_service: publisher_dependency,
    staff_user=Depends(get_staff_user),
) -> PublisherDTO | None:
    publisher = publisher_service.update(id=publisher_id, data=publisher)
    if publisher is None:
        raise HTTPException(status_code=404, detail="Издатель не был найден")
    return publisher
