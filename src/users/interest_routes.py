"""Interest routes for managing user interests."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.security import auth_user_dependency, db_dependency
from src.users.enums import UserRoleEnum
from src.users.schemas import CreateInterestRequestDTO, InterestResponseDTO, UpdateInterestRequestDTO
from src.users.services import InterestService

router = APIRouter(prefix="/user-interests", tags=["Interests"])


@router.post("/", response_model=InterestResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_interest(
    interest_data: CreateInterestRequestDTO, db: db_dependency, current_user: auth_user_dependency
):
    """Create a new interest. Only admins can create interests."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can create interests")

    return await InterestService.create_interest(interest_data, db)


@router.get("/", response_model=List[InterestResponseDTO])
async def get_all_interests(
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Get all active interests."""
    return await InterestService.get_all_interests(db)


@router.get("/{interest_id}", response_model=InterestResponseDTO)
async def get_interest_by_id(
    interest_id: UUID,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Get an interest by ID."""
    return await InterestService.get_interest_by_id(str(interest_id), db)


@router.put("/{interest_id}", response_model=InterestResponseDTO)
async def update_interest(
    interest_id: UUID,
    interest_data: UpdateInterestRequestDTO,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Update an interest. Only admins can update interests."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can update interests")

    return await InterestService.update_interest(str(interest_id), interest_data, db)


@router.delete("/{interest_id}")
async def delete_interest(
    interest_id: UUID,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Delete an interest (soft delete). Only admins can delete interests."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can delete interests")

    return await InterestService.delete_interest(str(interest_id), db)
