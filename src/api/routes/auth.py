from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.core.rate_limit import limiter
from src.schemas.auth import Token
from src.services.auth import login_for_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
@limiter.limit(
    "5/minute", error_message="Too many failed login attempts.Please try again later"
)
def login_for_access_token(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return login_for_token(db=db, username = form_data.username, password = form_data.password)