from typing import Annotated

from fastapi import APIRouter, Depends

from ..auth.dependencies import oauth2_scheme
from .schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    USERS = []
    return USERS
