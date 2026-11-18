from sqlmodel import SQLModel, Field
from .departments import Department
from datetime import datetime

class UserRole(SQLModel, table=True):
    __tablename__ = "roles"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=20, nullable=False)

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="departments.id")
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
    created_at: datetime = Field(default=None)