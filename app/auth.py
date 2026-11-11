from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.config import settings

ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("not-a-real-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str | None) -> bool:
    return password_hash.verify(password, hashed or DUMMY_HASH) and hashed is not None


def create_access_token(customer_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expire_minutes
    )
    return jwt.encode(
        {"sub": str(customer_id), "exp": expires},
        settings.jwt_secret.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(
        token, settings.jwt_secret.get_secret_value(), algorithms=[ALGORITHM]
    )
    return int(payload["sub"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_customer_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        return decode_access_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentCustomer = Annotated[int, Depends(get_current_customer_id)]
