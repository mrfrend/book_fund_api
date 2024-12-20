from sqlalchemy.orm import Session
from database.database import async_session_factory
from database.models import User
from sqlalchemy import select
from auth.utils import hash_password
from schemas.user import UserRoles, UserUpdateDTO


class UserRepository:
    def __init__(self, db_session: Session = async_session_factory):
        self.db_session = db_session

    async def find_one_or_none(self, username: str) -> User | None:
        async with self.db_session() as session:
            query = select(User).where(User.username == username)
            result = (await session.execute(query)).scalar_one_or_none()
            print(result)
            return result

    async def find_all(self) -> list[User]:
        async with self.db_session() as session:
            query = select(User)
            result = (await session.execute(query)).scalars().all()
            return result

    async def add(self, username: str, password: str):
        async with self.db_session() as session:
            hashed_password = hash_password(password)
            user = User(username=username, hashed_password=hashed_password)
            session.add(user)
            await session.commit()

    async def update_roles(self, user_id: int, roles: UserRoles) -> User | None:
        async with self.db_session() as session:
            user = session.get(User, user_id)
            if user is None:
                return
            user.is_user = roles.is_user
            user.is_admin = roles.is_admin
            user.is_staff = roles.is_staff
            await session.commit()
            await session.refresh(user)
            return user

    async def update_password(self, user_id: int, password: str) -> User | None:
        async with self.db_session() as session:
            user = await session.get(User, user_id)
            if user is None:
                return
            user.hashed_password = hash_password(password)
            await session.commit()
            await session.refresh(user)
            return user
        
    async def update_data(self,user_id: int, data: UserUpdateDTO) -> User | None:
        async with self.db_session() as session:
            user = await session.get(User, user_id)
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            await session.commit()
            await session.refresh(user)
            return user
