from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database.session import get_session
from app.core.security import get_current_user
from app.controllers.department_controllers import DepartmentController

router = APIRouter(prefix="/departments", tags=["Departments"])
@router.get("/", summary="Список отделов")
def get_all_departments(session: Session = Depends(get_session)):
    departments = DepartmentController.get_departments(session)
    if departments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отделы не найдены")
    return departments
