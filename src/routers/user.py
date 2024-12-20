from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from auth.dependancies import get_current_user, get_admin_user, get_current_user2
from auth.utils import validate_password
from database.models import User
from repositories.book_repository import BookRepository
from repositories.user_repository import UserRepository
from schemas.user import UserRoles, UserDTO, UpdatePasswordDTO, UserUpdateDTO
from services.services import BookService

router = APIRouter(prefix="/user", tags=["Управление пользователями"])
book_dependency = Annotated[BookService, Depends(BookService)]


@router.patch("/data", summary="Обновить данные пользователя")
async def update_data_user(data: UserUpdateDTO, user: User = Depends(get_current_user)):
    user_repository = UserRepository()
    user = await user_repository.update_data(user.id, data)
    if user is None:
        return {"message": "Пользователь не найден"}
    return UserDTO.model_validate(user, from_attributes=True)


@router.patch("/", summary="Обновить пароль пользователя")
async def update_password(
    data: UpdatePasswordDTO, user: User = Depends(get_current_user)
):
    if not validate_password(data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Неправильно введен нынешний пароль"
        )
    if data.new_password != data.new_password_repeat:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    user_repository = UserRepository()
    user = await user_repository.update_password(user.id, data.new_password)
    if user is None:
        return {"message": "Пользователь не найден"}
    return UserDTO.model_validate(user, from_attributes=True)


@router.patch("/{user_id:int}")
async def update_roles_user(
    user_id: int, roles: UserRoles, admin_user=Depends(get_admin_user)
):
    user_repository = UserRepository()
    user = await user_repository.update_roles(user_id, roles)
    if user is None:
        return {"message": "Пользователь не найден"}
    return UserDTO.model_validate(user, from_attributes=True)


@router.get("/desired-books", summary="Получить список желанных книг")
async def get_desired_books(
    book_service: book_dependency, user: User = Depends(get_current_user)
):
    return await book_service.get_desired_books(user.id)


@router.post("/desired/{book_id}", summary="Добавить книгу в желаемые пользователя")
async def add_book_to_desired(book_id: int, user: User = Depends(get_current_user)):
    try:
        await BookRepository().add_to_desired_book(book_id, user.id)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Ошибка добавления книги в избранное: {e}"
        )
    return {"message": "Книга добавлена в избранное"}


@router.delete("/desired/{book_id}", summary="Удалить книгу из избранного")
async def remove_book_from_desired(
    book_id: int, user: User = Depends(get_current_user)
):
    try:
        await BookRepository().remove_from_desired_book(book_id, user.id)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Ошибка удаления книги из избранного: {e}"
        )
    return {"message": "Книга удалена из избранного"}


@router.get("/generate-excel", summary="Сгенирировать отчет")
async def generate_excel():
    pass
