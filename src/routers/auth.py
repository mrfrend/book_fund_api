from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from schemas.user import UserAddDTO, TokenInfo, UserDTO
from repositories.user_repository import UserRepository
from database.models import User
from auth.utils import validate_password, encode_jwt, decode_jwt
from auth.dependancies import validate_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authorization, Авторизация"])


@router.post("/register", summary="Зарегистрироваться в системе")
def register_user(user_data: UserAddDTO):
    user_repository = UserRepository()
    user = user_repository.find_one_or_none(username=user_data.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    user_repository.add(**user_data.model_dump())
    return {"message": "Пользователь успешно зарегистрирован"}


@router.post("/login", summary="Войти в систему", response_model=TokenInfo)
def auth_user_jwt(response: Response, user: UserAddDTO = Depends(validate_user)):
    jwt_payload = {"sub": user.username}
    token = encode_jwt(jwt_payload)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return TokenInfo(access_token=token)


@router.post("/logout", summary="Выйти из системы")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Вы успешно вышли из системы"}


@router.get("/user/me", summary="Получить информацию о текущем пользователе")
def get_user_info(user: User = Depends(get_current_user)) -> UserDTO:
    return UserDTO.model_validate(user, from_attributes=True)

@router.get('/users', summary="Получить список всех пользователей")
def get_users():
    user_repository = UserRepository()
    users = user_repository.find_all()
    return [UserDTO.model_validate(user, from_attributes=True) for user in users]
