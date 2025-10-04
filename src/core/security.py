""" """

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.database import get_db
from src.core.schemas import AuthUser
from src.users.enums import UserRoleEnum
from src.users.models import User

logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/token")


def hash_password(password: str) -> str:
    """Hashes a password using the recommended hashing algorithm."""
    password_context = PasswordHash.recommended()
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    password_context = PasswordHash.recommended()
    return password_context.verify(plain_password, hashed_password)


async def authenticate_user_with_username(username: str, password: str, db: AsyncSession) -> User | bool:
    """Authenticates a user by checking the username and password."""

    result = await db.execute(select(User).where(User.username == username))
    user: User = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def authenticate_user_with_phone(phone: str, password: str, db: AsyncSession) -> User | bool:
    """Authenticates a user by checking the username and password."""

    result = await db.execute(select(User).where(User.phone == phone))
    user: User = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(user: User, expires_delta: timedelta = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """Creates an access token with the given data and expiration time."""

    encode_token = {"sub": f"{user.id}", "username": user.username, "role": user.role, "full_name": user.full_name}
    expires = datetime.now(timezone.utc) + expires_delta
    encode_token.update({"exp": expires})
    return jwt.encode(encode_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def __get_invalid_credentials_exception_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Estas credências são inválidas!",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Returns a dictionary with user data."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        raise __get_invalid_credentials_exception_error()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> AuthUser:
    """Returns a AuthUser with essential user data."""

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user: AuthUser = AuthUser(
            id=payload.get("sub"),
            full_name=payload.get("full_name"),
            role=payload.get("role"),
            username=payload.get("username"),
        )

        if user.id is None or user.username is None:
            raise __get_invalid_credentials_exception_error()
        return user
    except PyJWTError:
        raise __get_invalid_credentials_exception_error()
    except Exception as e:
        logger.exception(e)
        raise __get_invalid_credentials_exception_error()


def get_super_admin_user(current_user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
    """Returns a dictionary with user data."""

    if current_user.role == UserRoleEnum.SUPER_ADMIN or current_user.role == UserRoleEnum.SUPER_ADMIN:
        return current_user
    name = current_user.full_name.split(" ")[0]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Ups!! Lamentamos {name}😢, mas você não tem permissão para realizar essa acção no sistema!",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_admin_user(current_user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
    """Returns a AuthUser with essential admin data."""

    if current_user.role in [UserRoleEnum.ADMIN.value, UserRoleEnum.SUPER_ADMIN.value]:
        return current_user
    name = current_user.full_name.split(" ")[0]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Ups!! Lamentamos {name}😢, mas você não tem permissão para realizar essa acção no sistema!",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_pro_user(current_user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
    """Returns a dictionary with user data."""

    if current_user.role == UserRoleEnum.ADMIN or current_user.role == UserRoleEnum.PROFESSIONAL:
        return current_user
    name = current_user.full_name.split(" ")[0]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Ups!! Lamentamos {name}😢, mas você não tem permissão para realizar essa acção no sistema!",
        headers={"WWW-Authenticate": "Bearer"},
    )


db_dependency = Annotated[AsyncSession, Depends(get_db)]
super_admin_user_dependency = Annotated[AuthUser, Depends(get_super_admin_user)]
admin_user_dependency = Annotated[AuthUser, Depends(get_admin_user)]
pro_user_dependency = Annotated[AuthUser, Depends(get_pro_user)]
auth_user_dependency = Annotated[AuthUser, Depends(get_current_user)]


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ) -> User:
#     """Returns the current active user."""
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive user",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     return current_user
