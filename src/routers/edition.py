from fastapi import APIRouter, Depends, HTTPException
from services import EditionService
from schemas.editions import EditionDTO, EditionAddDTO, EditionUpdateDTO, EditionRelDTO
from dependacies import get_edition_service
from typing import Annotated

router = APIRouter(prefix="/editions", tags=["Издания, Editions"])
edition_dependency = Annotated[EditionService, Depends(get_edition_service)]


@router.get("/", summary="Получить все издания")
def get_all_editions(edition_service: edition_dependency) -> list[EditionRelDTO]:
    editions = edition_service.get_all()
    return editions


@router.get("/{edition_id}", summary="Получить издание по id")
def get_edition(
    edition_id: int, edition_service: edition_dependency
) -> EditionDTO | None:
    edition = edition_service.get(id=edition_id)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition


@router.post("/", summary="Добавить издание")
def add_edition(
    edition: EditionAddDTO, edition_service: edition_dependency
) -> EditionDTO:
    edition = edition_service.create(edition)
    return edition


@router.delete("/{edition_id}", summary="Удалить издание по id")
def delete_edition(edition_id: int, edition_service: edition_dependency):
    res = edition_service.delete(id=edition_id)
    if res:
        return {"message": "Издание удалено"}
    else:
        raise HTTPException(status_code=404, detail="Издание не было найдено")


@router.patch("/{edition_id}", summary="Обновить издание по id")
def update_edition(
    edition_id: int, edition: EditionUpdateDTO, edition_service: edition_dependency
) -> EditionDTO | None:
    edition = edition_service.update(id=edition_id, data=edition)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition
