"""Security module for handling password hashing, token creation, and user authentication."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import (
    SignInWithPhoneNumberRequestDTO,
    SignInWithUsernameRequestDTO,
    TokenResponseDTO,
    VerifyTokenRequestDTO,
)
from src.core.config import settings
from src.core.security import (
    auth_user_dependency,
    authenticate_user_with_phone,
    authenticate_user_with_username,
    create_access_token,
    db_dependency,
    verify_token,
)
from src.users.schemas import UpdateUserRequestDTO, UserChangePasswordRequestDTO, UserResponseDTO
from src.users.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

# ----------------------------------------------------------
# AUTHENTICATION ENDPOINTS
# ----------------------------------------------------------


@router.put("/me/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_dto: Annotated[UserChangePasswordRequestDTO, Body()], db: db_dependency, current_user: auth_user_dependency
):
    """Change current user's password."""
    await UserService.change_password(current_user=current_user, password_dto=password_dto, db=db)
    return {"message": "Senha alterada com sucesso"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: auth_user_dependency):
    """Logout user (invalidate token on client side)."""
    # In a real implementation, you might want to blacklist the token
    # For now, we just return a success message as the client should remove the token
    return {"message": "Logout realizado com sucesso"}


@router.post("/token-phone", response_model=TokenResponseDTO)
async def login_with_phone_number(user_data: Annotated[SignInWithPhoneNumberRequestDTO, Body()], db: db_dependency):
    """Returns the generated tokens (JWTs)"""
    user = await authenticate_user_with_phone(phone=user_data.phone, password=user_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Estas credências são inválidas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/verify-token", status_code=status.HTTP_200_OK)
async def token_verification(token_data: Annotated[VerifyTokenRequestDTO, Body()]):
    """Verifies the access token and returns a new token if valid."""
    verify_token(token_data.token)
    return {"message": "Token verificado com sucesso"}


@router.post("/token", response_model=TokenResponseDTO)
async def login_with_username(user_data: Annotated[SignInWithUsernameRequestDTO, Body()], db: db_dependency):
    """Returns the generated tokens (JWTs)"""
    user = await authenticate_user_with_username(username=user_data.username, password=user_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/form-token", response_model=TokenResponseDTO)
async def login_request_form_access_token(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    """Returns the JWT token from form request."""
    user = await authenticate_user_with_username(username=user_data.username, password=user_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "Bearer"}
