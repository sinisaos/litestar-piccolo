from pydantic import BaseModel, EmailStr


class UserModelRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserModelLogin(BaseModel):
    username: str
    password: str
