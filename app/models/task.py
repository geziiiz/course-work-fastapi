from sqlmodel import SQLModel, Field
from .departments import Department
from datetime import date

class TaskStatus(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50, nullable=False)
class TaskPriority(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50, nullable=False)

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: str = Field(max_length=1000)
    status_id: int = Field(foreign_key="task_statuses.id")
    priority_id: int = Field(foreign_key="task_priorities.id")
    deadline: date = Field(default=None)
    created_at: date = Field(default=None)
    completed_at: date = Field(default=None)
    author_id: int = Field(foreign_key="user.id")
    assignee_id: int = Field(foreign_key="user.id")