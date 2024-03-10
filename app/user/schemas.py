from datetime import (
    date,
    datetime,
)
from pydantic import (
    BaseModel,
    EmailStr,
)


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    username: str
    email: EmailStr
    phone: str
    full_name: str
    birthday: date


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str
    full_name: str
    birthday: date


class UserUpdate(BaseModel):
    password: str
    email: EmailStr
    phone: str
    full_name: str
    birthday: date


class UserLogin(BaseModel):
    account: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str
    full_name: str
    birthday: date
