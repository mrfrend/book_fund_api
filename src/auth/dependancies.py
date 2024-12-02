from fastapi import Depends, Form, HTTPException, status, Request
from jwt import InvalidTokenError
from repositories.user_repository import UserRepository
from database.models import User
from auth.utils import decode_jwt, validate_password
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def validate_user(username: str = Form(), password: str = Form()):
    user_repository = UserRepository()
    user: User = await user_repository.find_one_or_none(username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден"
        )
    if not validate_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
        )
    return user


# def get_token(request: Request):
#     token = request.cookies.get("access_token")
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима авторизация"
#         )
#     return token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}"
        )
    user_repository = UserRepository()
    user = await user_repository.find_one_or_none(username=payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден"
        )
    return user

def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не является админом."
        )
    return user

def get_staff_user(user: User = Depends(get_current_user)):
    if not user.is_staff and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не является сотрудником или админом."
        )
    return user

