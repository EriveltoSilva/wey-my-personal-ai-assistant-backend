"""Professional Area routes for managing professional areas."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.security import auth_user_dependency, db_dependency
from src.users.enums import UserRoleEnum
from src.users.schemas import (
    CreateProfessionalAreaRequestDTO,
    ProfessionalAreaResponseDTO,
    UpdateProfessionalAreaRequestDTO,
)
from src.users.services import ProfessionalAreaService

router = APIRouter(prefix="/professional-areas", tags=["Professional Areas"])


@router.post("/", response_model=ProfessionalAreaResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_professional_area(
    area_data: CreateProfessionalAreaRequestDTO,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Create a new professional area. Only admins can create professional areas."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can create professional areas"
        )

    return await ProfessionalAreaService.create_professional_area(area_data, db)


@router.get("/", response_model=List[ProfessionalAreaResponseDTO])
async def get_all_professional_areas(
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Get all active professional areas."""
    return await ProfessionalAreaService.get_all_professional_areas(db)


@router.get("/{area_id}", response_model=ProfessionalAreaResponseDTO)
async def get_professional_area_by_id(
    area_id: UUID,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Get a professional area by ID."""
    return await ProfessionalAreaService.get_professional_area_by_id(str(area_id), db)


@router.put("/{area_id}", response_model=ProfessionalAreaResponseDTO)
async def update_professional_area(
    area_id: UUID,
    area_data: UpdateProfessionalAreaRequestDTO,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Update a professional area. Only admins can update professional areas."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can update professional areas"
        )

    return await ProfessionalAreaService.update_professional_area(str(area_id), area_data, db)


@router.delete("/{area_id}")
async def delete_professional_area(
    area_id: UUID,
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Delete a professional area (soft delete). Only admins can delete professional areas."""
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can delete professional areas"
        )

    return await ProfessionalAreaService.delete_professional_area(str(area_id), db)
