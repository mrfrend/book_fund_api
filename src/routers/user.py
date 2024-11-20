from fastapi import APIRouter, Depends
from auth.dependancies import get_admin_user
from repositories.user_repository import UserRepository
from schemas.user import UserRoles, UserDTO

router = APIRouter(prefix="/user", tags=["Управление пользователями"])


@router.patch("/{user_id}")
def update_roles_user(user_id: int, roles: UserRoles, admin_user = Depends(get_admin_user)):
    user_repository = UserRepository()
    user = user_repository.update_roles(user_id, roles)
    if user is None:
        return {"message": "Пользователь не найден"}
    return UserDTO.model_validate(user, from_attributes=True)
