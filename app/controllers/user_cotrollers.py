import logging
from sqlmodel import Session, select, delete
from app.models.user import User

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
    