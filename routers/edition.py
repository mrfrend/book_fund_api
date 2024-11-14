from fastapi import APIRouter, Depends, HTTPException
from repositories.edition_repository import EditionRepository
from schemas.editions import EditionDTO, EditionAddDTO, EditionUpdateDTO
from dependacies import get_edition_repository
from typing import Annotated

router = APIRouter(prefix="/editions", tags=["Издания, Editions"])
edition_dependency = Annotated[EditionRepository, Depends(get_edition_repository)]


@router.get("/", summary="Получить все издания")
def get_all_editions(repo: edition_dependency) -> list[EditionDTO]:
    return repo.get_all()


@router.get("/{edition_id}", summary="Получить издание по id")
def get_edition(edition_id: int, repo: edition_dependency) -> EditionDTO | None:
    edition = repo.get(id=edition_id)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition


@router.post("/", summary="Добавить издание")
def add_edition(edition: EditionAddDTO, repo: edition_dependency) -> EditionDTO:
    edition = repo.create(edition)
    return edition


@router.delete("/{edition_id}", summary="Удалить издание по id")
def delete_edition(edition_id: int, repo: edition_dependency):
    res = repo.delete(id=edition_id)
    if res:
        return {"message": "Издание удалено"}
    else:
        raise HTTPException(status_code=404, detail="Издание не было найдено")


@router.patch("/{edition_id}", summary="Обновить издание по id")
def update_edition(
    edition_id: int, edition: EditionUpdateDTO, repo: edition_dependency
) -> EditionDTO | None:
    edition = repo.update(id=edition_id, data=edition)
    if edition is None:
        raise HTTPException(status_code=404, detail="Издание не было найдено")
    return edition
