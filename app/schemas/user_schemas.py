from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    surname: str = Field(max_length=50)
    name: str = Field(max_length=50)
    patronymic: str | None = Field(max_length=50)
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=8)
    role_id: int = Field()
    department_id:int = Field()
class UserRead(UserBase):
    id: int
    role_id: int
    department_id: int
    model_config = ConfigDict(from_attributes=True)
class UserUpdate(BaseModel):
    password: str | None = Field(min_length=8)
    role_id: int | None = Field()
    department_id:int | None = Field()