from pydantic import BaseModel, Field


class UserAddDTO(BaseModel):
    username: str
    password: str = Field(max_length=20)


class UserDTO(UserAddDTO):
    id: int
    is_user: bool = True
    is_admin: bool = False
    is_staff: bool = False
    password: str = Field(alias='hashed_password')

class UserRoles(BaseModel):
    is_user: bool | None = True
    is_admin: bool | None = False
    is_staff: bool | None = False



class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"
