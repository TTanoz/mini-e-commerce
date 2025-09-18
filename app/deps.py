from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .core import security

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(security.oauth2_scheme)],
) -> User:
    try:
        data = security.decode_token(token)
        uid = int(data.get("sub", "0"))
    except Exception:
        raise credentials_exception
    user = db.get(User, uid)
    if not user:
        raise credentials_exception
    if getattr(user, "is_active", True) is False:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

def get_current_user_id(
    user: Annotated[User, Depends(get_current_user)]
) -> int:
    return user.id

def get_current_user_email(
    user: Annotated[User, Depends(get_current_user)]
) -> str:
    return user.email
