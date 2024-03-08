from datetime import (
    date,
    datetime
)
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)
from typing import Optional


class Register(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str
    full_name: str
    birthday: date


class Login(BaseModel):
    account: str
    password: str


class Session(BaseModel):
    id: str
    data: dict


class VerifyOTP(BaseModel):
    OTP: str

    @field_validator("OTP")
    def check_OTP_length(cls, value):
        if len(value) != 6:
            raise ValueError('invalid OTP')
