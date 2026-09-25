from pydantic import BaseModel

from app.features.users.roles import UserRoles


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserRead(BaseModel):
    id_: int
    name: str
    email: str
    role: UserRoles
    is_demo: bool
    is_active: bool 

