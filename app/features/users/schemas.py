from pydantic import BaseModel

from app.features.users.roles import UserRoles


class User(BaseModel):
    id_: int
    name: str
    email: str
    password: str
    role: UserRoles = "user"


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserRead(BaseModel):
    name: str
    email: str
