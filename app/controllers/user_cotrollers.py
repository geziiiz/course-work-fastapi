import logging
from sqlmodel import Session, select, delete
from app.models.user import User
from app.schemas.user_schemas import *

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User:
        try:
            return session.get(User, user_id)
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None
    @staticmethod
    def get_all_users(session: Session) -> list[User]:
        try:
            return list(session.exec(select(User)).all())
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            return None
    @staticmethod
    def add_user(data: UserCreate, session: Session):
        """Создаёт профиль. None — если email уже занят."""
        try:
            existing = session.exec(
                select(User).where(User.email == data.email)
            ).first()
            if existing:
                logger.warning(f"Cannot add profile: email {data.email} is already taken")
                return None

            profile = User(
                email=data.email,
                password=data.password,
                surname=data.surname,
                name=data.name,
                patronymic=data.patronymic,
                role_id=data.role_id,
                department_id=data.department_id
            )
            session.add(profile)
            session.commit()
            session.refresh(profile)
            return profile

        except Exception as e:
            session.rollback()
            logger.exception(f"Cannot add user: {repr(e)}")
            return None

