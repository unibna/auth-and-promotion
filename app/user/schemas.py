from datetime import (
    date,
)
from pydantic import (
    BaseModel,
    EmailStr,
)


class UserResponse(BaseModel):
    id: int
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
