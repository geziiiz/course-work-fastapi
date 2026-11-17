from sqlmodel import SQLModel, Field
from .departments import Department
from datetime import date

class UserRole(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=20, nullable=False)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    department_id: str = Field(foreign_key="departments.id")
    role_id: int = Field(foreign_key="roles.id")
    surname: str = Field(max_length=100, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    patronymic: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=100, nullable=False)
    phone: str = Field(unique=True, max_length=20)
    passport_series: str = Field(unique=True, max_length=10)
    passport_number: str = Field(unique=True, max_length=10)
    inn: str = Field(unique=True, max_length=12)
    snils: str = Field(unique=True, max_length=15)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: date = Field(default=None)