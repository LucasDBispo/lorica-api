from typing import Annotated

from fastapi import APIRouter, Depends

from app.features.users.dependencies import create_user, get_all_users

from .schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def get_users():
    users = get_all_users()
    return users


@router.post("/", response_model=UserCreate)
async def create_new_user(user: Annotated[UserCreate, Depends(create_user)]):
    return user
