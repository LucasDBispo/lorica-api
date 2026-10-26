from enum import Enum

from pydantic import BaseModel


class UserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: UserRoles
    is_demo: bool
    is_active: bool 
