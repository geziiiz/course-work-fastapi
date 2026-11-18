from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.session import get_session
from app.controllers.user_cotrollers import UserController
from app.schemas.user_schemas import *

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", summary="Список пользователей")
def get_all_users(session: Session = Depends(get_session)):
    users = UserController.get_all_users(session)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователи не найдены")
    return users
@router.get("/{user_id}", summary="Получить пользователя по ID")
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = UserController.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user
@router.post("/register", response_model=UserRead, status_code=201)
def post_user(data: UserCreate, session: Session = Depends(get_session)):
    user = UserController.add_user(data, session)
    if user is None:
        raise HTTPException(409, f"Email '{data.email}' уже занят")
    return user