from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ...controllers.user_cotrollers import UserController
from ...core.security import create_access_token, create_refresh_token
from sqlmodel import Session
from ...database.session import get_session
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = UserController.authenticate(
        email=form_data.username,
        user_password=form_data.password,
        session=session
    )
    if user is None:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
            )
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
    }
@router.get("/users/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user