import logging
from sqlmodel import Session, select, delete
from app.models.user import User
from app.schemas.user_schemas import *
from app.core.security import hash_password

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
                password=hash_password(data.password),
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
    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        """Удаляет профиль. True — если удаление прошло успешно."""
        try:
            user = session.get(User, user_id)
            if not user:
                logger.warning(f"Cannot delete profile: user with ID {user_id} does not exist")
                return False

            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.exception(f"Cannot delete user with ID {user_id}: {repr(e)}")
            return False
    @staticmethod
    def update_user(session: Session, user_id: int, data: UserUpdate) -> User:
        """Обновляет профиль. None — если пользователь не найден."""
        try:
            user = session.get(User, user_id)
            if not user:
                logger.warning(f"Cannot update profile: user with ID {user_id} does not exist")
                return None

            for key, value in data.dict(exclude_unset=True).items():
                setattr(user, key, value)

            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            logger.exception(f"Cannot update user with ID {user_id}: {repr(e)}")
            return None