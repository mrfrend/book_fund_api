from fastapi import APIRouter, Depends, HTTPException
from services import EditionService
from schemas import (
    EditionDTO,
    EditionAddDTO,
    EditionUpdateDTO,
    EditionRelDTO,
)
from typing import Annotated
from auth.dependancies import get_staff_user

router = APIRouter(prefix="/editions", tags=["Издания, Editions"])
edition_dependency = Annotated[EditionService, Depends(EditionService)]


@router.get("/", summary="Получить все издания")
async def get_all_editions(edition_service: edition_dependency) -> list[EditionRelDTO]:
    editions = await edition_service.get_all()
    return editions


@router.get("/{edition_id}", summary="Получить издание по id")
async def get_edition(
    edition_id: int, edition_service: edition_dependency
) -> EditionRelDTO | None:
    edition = await edition_service.get(id=edition_id)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition


@router.post("/", summary="Добавить издание")
async def add_edition(
    edition: EditionAddDTO,
    edition_service: edition_dependency,
    staff_user=Depends(get_staff_user),
) -> EditionDTO:
    edition = await edition_service.create(edition)
    return edition


@router.delete("/{edition_id}", summary="Удалить издание по id")
async def delete_edition(
    edition_id: int,
    edition_service: edition_dependency,
    staff_user=Depends(get_staff_user),
):
    res = await edition_service.delete(id=edition_id)
    if res:
        return {"message": "Издание удалено"}
    else:
        raise HTTPException(status_code=404, detail="Издание не было найдено")


@router.patch("/{edition_id}", summary="Обновить издание по id")
async def update_edition(
    edition_id: int,
    edition: EditionUpdateDTO,
    edition_service: edition_dependency,
    staff_user=Depends(get_staff_user),
) -> EditionDTO | None:
    edition = await edition_service.update(id=edition_id, data=edition)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition
