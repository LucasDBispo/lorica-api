from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.features.auth.dependencies import oauth2_scheme
from app.features.users.dependencies import create_user, get_user_by_token
from app.features.users.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    return get_user_by_token(db=db, token=token)


@router.get("/", response_model=list[UserRead])
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    USERS = []
    return USERS


@router.post("/", status_code=201, response_model=UserRead)
async def register_user(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return create_user(user_data, db)
