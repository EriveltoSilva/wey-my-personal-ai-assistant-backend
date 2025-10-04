"""FastAPI routes for user management."""

import json
from typing import Annotated

from fastapi import APIRouter, Body, File, HTTPException, Path, Query, UploadFile, status

from src.core.schemas import FilterParams
from src.core.security import auth_user_dependency, db_dependency, super_admin_user_dependency
from src.users.models import User
from src.users.schemas import (
    AvatarUploadResponseDTO,
    CreateProfileRequestDTO,
    CreateUserRequestDTO,
    OnboardingQuestionnaireDTO,
    ProfileResponseDTO,
    UpdateProfileRequestDTO,
    UpdateUserRequestDTO,
    UserProfessionalProfileUpdateDTO,
    UserResponseDTO,
    UserWithRelationsResponseDTO,
)
from src.users.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponseDTO], status_code=status.HTTP_200_OK)
async def get_all_users(
    db: db_dependency, current_user: super_admin_user_dependency, filter_params: Annotated[FilterParams, Query()] = None
):
    return await UserService.get_all_users(filter_params, db)


@router.post("", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(user_dto: Annotated[CreateUserRequestDTO, Body()], db: db_dependency):
    """Create a new user."""
    return await UserService.create_user(user_dto=user_dto, db=db)


@router.get("/me", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
async def read_user(db: db_dependency, current_user: auth_user_dependency):
    """Get a user by ID."""
    return await UserService.me(current_user=current_user, db=db)


@router.put("/me", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
async def update_my_profile(
    user_dto: Annotated[UpdateUserRequestDTO, Body()], db: db_dependency, current_user: auth_user_dependency
):
    """Update current user's profile."""
    return await UserService.update_user(user_id=current_user.id, current_user=current_user, user_dto=user_dto, db=db)


@router.get("/{user_id}", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
async def read_user(user_id: str, db: db_dependency, current_user: auth_user_dependency):
    """Get a user by ID."""
    return await UserService.read_user(user_id=user_id, current_user=current_user, db=db)


@router.put("/{user_id}", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: Annotated[str, Path()],
    user_dto: Annotated[UpdateUserRequestDTO, Body()],
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Update a user by ID."""
    return await UserService.update_user(user_id=user_id, current_user=current_user, user_dto=user_dto, db=db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: Annotated[str, Path()], db: db_dependency, current_user: auth_user_dependency):
    """Delete a user by ID."""
    return await UserService.delete_user(user_id=user_id, current_user=current_user, db=db)


# Avatar Management Endpoints
@router.post("/me/avatar", response_model=AvatarUploadResponseDTO, status_code=status.HTTP_200_OK)
async def upload_avatar(
    db: db_dependency,
    current_user: auth_user_dependency,
    file: UploadFile = File(..., description="Avatar image file (JPEG, PNG, GIF, WebP, max 5MB)"),
):
    """Upload and update user avatar."""
    return await UserService.upload_avatar(current_user=current_user, file=file, db=db)


@router.get("/me/profile-details", response_model=UserWithRelationsResponseDTO, status_code=status.HTTP_200_OK)
async def get_my_profile(db: db_dependency, current_user: auth_user_dependency):
    """Get current user with all related data (profile, address)."""
    return await UserService.get_user_with_relations(current_user=current_user, db=db)


# Professional Profile and Onboarding Endpoints
@router.post("/me/onboarding", status_code=status.HTTP_200_OK)
async def complete_onboarding(
    onboarding_data: Annotated[OnboardingQuestionnaireDTO, Body()],
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Complete user onboarding questionnaire."""
    return await UserService.complete_onboarding(user_id=current_user.id, onboarding_data=onboarding_data, db=db)


@router.get("/me/onboarding-status", status_code=status.HTTP_200_OK)
async def get_onboarding_status(db: db_dependency, current_user: auth_user_dependency):
    """Get user onboarding completion status."""
    return {
        "onboarding_completed": current_user.onboarding_completed,
        "professional_profile": current_user.get_professional_profile(),
    }


# @router.put("/me/professional-profile", status_code=status.HTTP_200_OK)
# async def update_professional_profile(
#     profile_data: Annotated[UserProfessionalProfileUpdateDTO, Body()],
#     db: db_dependency,
#     current_user: auth_user_dependency,
# ):
#     """Update user professional profile."""
#     return await UserService.update_professional_profile(user_id=current_user.id, profile_data=profile_data, db=db)


# @router.get("/me/professional-profile", status_code=status.HTTP_200_OK)
# async def get_professional_profile(db: db_dependency, current_user: auth_user_dependency):
#     """Get user professional profile."""
#     return current_user.get_professional_profile()
