from pydantic import BaseModel, Field


class UserAddDTO(BaseModel):
    username: str
    password: str = Field(max_length=20)
    first_name: str | None = Field(max_length=25, default=None)
    last_name: str | None = Field(max_length=50, default=None)


class UserDTO(UserAddDTO):
    id: int
    password: str = Field(alias="hashed_password")
    is_admin: bool | None = False


class UserRoles(BaseModel):
    is_user: bool | None = True
    is_admin: bool | None = False
    is_staff: bool | None = False


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UpdatePasswordDTO(BaseModel):
    old_password: str
    new_password: str
    new_password_repeat: str

class UserUpdateDTO(BaseModel):
    first_name: str | None = Field(max_length=25, default=None)
    last_name: str | None = Field(max_length=50, default=None)
