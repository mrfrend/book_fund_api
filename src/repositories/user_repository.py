from sqlalchemy.orm import Session
from database.database import session_factory
from database.models import User
from sqlalchemy import select
from auth.utils import hash_password
from schemas.user import UserRoles


class UserRepository:
    def __init__(self, db_session: Session = session_factory):
        self.db_session = db_session

    def find_one_or_none(self, username: str) -> User | None:
        with self.db_session() as session:
            query = select(User).where(User.username == username)
            result = session.execute(query).scalar_one_or_none()
            print(result)
            return result
    
    def find_all(self) -> list[User]:
        with self.db_session() as session:
            query = select(User)
            result = session.execute(query).scalars().all()
            return result


    def add(self, username: str, password: str):
        with self.db_session() as session:
            hashed_password = hash_password(password)
            user = User(username=username, hashed_password=hashed_password)
            session.add(user)
            session.commit()

    def update_roles(self, user_id: int, roles: UserRoles) -> User | None:
        with self.db_session() as session:
            user = session.get(User, user_id)
            if user is None:
                return
            user.is_user = roles.is_user
            user.is_admin = roles.is_admin
            user.is_staff = roles.is_staff
            session.commit()
            session.refresh(user)
            return user
