import logging
from sqlmodel import Session, select, delete
from app.models.user import User
from app.models.departments import Department
from app.schemas.user_schemas import *
from app.core.security import hash_password, verify_password

class DepartmentController:
    @staticmethod
    def get_departments(session: Session) -> list[Department]:
        """Возвращает список всех отделов"""
        try:
            return list(session.exec(select(Department)).all())
        except Exception as e:
            logging.error(f"Error fetching all departments: {e}")
            return None
    @staticmethod
    def create_department(session: Session, data: Department) -> Department:
        """Создает отдел"""
        try:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data
        except Exception as e:
            logging.error(f"Ошибка создания отдела: {e}")
            return None
    @staticmethod
    def update_department(session: Session, department_id: int, data: Department) -> Department:
        """Обновляет отдел"""
        try:
            department = session.get(Department, department_id)
            if not department:
                logging.warning(f"Отдел с ID {department_id} не найден для обновления")
                return None
            for key, value in data.dict(exclude_unset=True).items():
                setattr(department, key, value)
            session.commit()
            session.refresh(department)
            return department
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка обновления отдела с ID {department_id}: {e}")
            return None
    @staticmethod
    def delete_department(session: Session, department_id: int) -> bool:
        """Удаляет отдел"""
        try:
            department = session.get(Department, department_id)
            if not department:
                logging.warning(f"Отдел с ID {department_id} не найден для удаления")
                return False
            session.delete(department)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка удаления отдела с ID {department_id}: {e}")
            return False
    @staticmethod
    def attach_user_to_department(session: Session, user_id: int, department_id: int) -> bool:
        """Привязывает пользователя к отделу"""
        try:
            user = session.get(User, user_id)
            department = session.get(Department, department_id)
            if not user or not department:
                logging.warning(f"Такой пользователь или отдел не найден (user_id: {user_id}, department_id: {department_id})")
                return False
            user.department_id = department_id
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка привязки пользователя с ID {user_id} к отделу с ID {department_id}: {e}")
            return False
        