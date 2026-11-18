from sqlmodel import SQLModel, Field
from .departments import Department
from datetime import date, datetime

class TaskStatus(SQLModel, table=True):
    __tablename__ = "task_statuses"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50, nullable=False)
class TaskPriority(SQLModel, table=True):
    __tablename__ = "task_priorities"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50, nullable=False)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: str = Field(max_length=1000)
    status_id: int = Field(foreign_key="task_statuses.id")
    priority_id: int = Field(foreign_key="task_priorities.id")
    deadline: date = Field(default=None)
    created_at: datetime = Field(default=None)
    completed_at: datetime = Field(default=None)
    author_id: int = Field(foreign_key="user.id")
    assignee_id: int = Field(foreign_key="user.id")