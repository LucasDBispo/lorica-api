from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user, get_db
from src.core.rate_limit import limiter
from src.repositories.user import create_user
from src.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def read_users_me(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    return current_user


@router.post("/", status_code=201)
@limiter.limit("3/minute", error_message="Too many requests. Please try again later.")
async def register_user(
    request: Request,
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return create_user(user_in, db)
