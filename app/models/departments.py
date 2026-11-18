from sqlmodel import SQLModel, Field

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)