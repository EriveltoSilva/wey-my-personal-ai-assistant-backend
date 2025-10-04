"""service"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.core.schemas import AuthUser, FilterParams
from src.core.security import hash_password, verify_password
from src.exceptions import NotFoundException, UnauthorizedException
from src.users.enums import UserRoleEnum
from src.users.models import Interest, ProfessionalArea, User
from src.users.schemas import (
    CreateInterestRequestDTO,
    CreateProfessionalAreaRequestDTO,
    CreateUserRequestDTO,
    InterestResponseDTO,
    OnboardingQuestionnaireDTO,
    ProfessionalAreaResponseDTO,
    UpdateInterestRequestDTO,
    UpdateProfessionalAreaRequestDTO,
    UpdateUserRequestDTO,
    UserChangePasswordRequestDTO,
    UserProfessionalProfileUpdateDTO,
)


class ProfessionalAreaService:
    """Professional Area service for managing professional areas."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_professional_area(
        self, area_data: CreateProfessionalAreaRequestDTO
    ) -> ProfessionalAreaResponseDTO:
        """Create a new professional area."""
        # Check if professional area with the same name already exists
        result = await self.db.execute(select(ProfessionalArea).where(ProfessionalArea.name == area_data.name))
        existing_area = result.scalar_one_or_none()

        if existing_area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area with this name already exists"
            )

        # Check if code already exists (if provided)
        if area_data.code:
            result = await self.db.execute(select(ProfessionalArea).where(ProfessionalArea.code == area_data.code))
            existing_code = result.scalar_one_or_none()

            if existing_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area with this code already exists"
                )

        new_area = ProfessionalArea(
            name=area_data.name,
            description=area_data.description,
            code=area_data.code,
        )

        self.db.add(new_area)
        await self.db.commit()
        await self.db.refresh(new_area)

        return ProfessionalAreaResponseDTO.model_validate(new_area)

    async def get_all_professional_areas(self) -> List[ProfessionalAreaResponseDTO]:
        """Get all active professional areas."""
        result = await self.db.execute(
            select(ProfessionalArea).where(ProfessionalArea.is_active == True).order_by(ProfessionalArea.name)
        )
        areas = result.scalars().all()
        return [ProfessionalAreaResponseDTO.model_validate(area) for area in areas]

    async def get_professional_area_by_id(self, area_id: str) -> ProfessionalAreaResponseDTO:
        """Get professional area by ID."""
        area = await self.db.get(ProfessionalArea, area_id)
        if not area:
            raise NotFoundException("Área profissional não encontrada")
        return ProfessionalAreaResponseDTO.model_validate(area)

    async def update_professional_area(
        self, area_id: str, area_data: UpdateProfessionalAreaRequestDTO
    ) -> ProfessionalAreaResponseDTO:
        """Update an existing professional area."""
        area = await self.db.get(ProfessionalArea, area_id)
        if not area:
            raise NotFoundException("Professional area not found")

        # Check if another area with the same name exists (if name is being updated)
        if area_data.name and area_data.name != area.name:
            result = await self.db.execute(select(ProfessionalArea).where(ProfessionalArea.name == area_data.name))
            existing_area = result.scalar_one_or_none()
            if existing_area:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area with this name already exists"
                )

        # Check if another area with the same code exists (if code is being updated)
        if area_data.code and area_data.code != area.code:
            result = await self.db.execute(select(ProfessionalArea).where(ProfessionalArea.code == area_data.code))
            existing_code = result.scalar_one_or_none()
            if existing_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area with this code already exists"
                )

        # Update fields that are provided
        if area_data.name is not None:
            area.name = area_data.name
        if area_data.description is not None:
            area.description = area_data.description
        if area_data.code is not None:
            area.code = area_data.code
        if area_data.is_active is not None:
            area.is_active = area_data.is_active

        await self.db.commit()
        await self.db.refresh(area)

        return ProfessionalAreaResponseDTO.model_validate(area)

    async def delete_professional_area(self, area_id: str) -> Dict[str, str]:
        """Soft delete a professional area by setting is_active to False."""
        area = await self.db.get(ProfessionalArea, area_id)
        if not area:
            raise NotFoundException("Professional area not found")

        area.is_active = False
        await self.db.commit()

        return {"message": "Professional area deleted successfully"}


class InterestService:
    """Interest service for managing user interests."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_interest(self, interest_data: CreateInterestRequestDTO) -> InterestResponseDTO:
        """Create a new interest."""
        # Check if interest with the same name already exists
        result = await self.db.execute(select(Interest).where(Interest.name == interest_data.name))
        existing_interest = result.scalar_one_or_none()

        if existing_interest:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interest with this name already exists",
            )

        new_interest = Interest(
            name=interest_data.name,
            description=interest_data.description,
            category=interest_data.category,
        )

        self.db.add(new_interest)
        await self.db.commit()
        await self.db.refresh(new_interest)

        return InterestResponseDTO.model_validate(new_interest)

    async def get_all_interests(self) -> List[InterestResponseDTO]:
        """Get all active interests."""
        result = await self.db.execute(select(Interest).where(Interest.is_active == True).order_by(Interest.name))
        interests = result.scalars().all()
        return [InterestResponseDTO.model_validate(interest) for interest in interests]

    async def get_interest_by_id(self, interest_id: str) -> InterestResponseDTO:
        """Get interest by ID."""
        interest = await self.db.get(Interest, interest_id)
        if not interest:
            raise NotFoundException("Interest not found")
        return InterestResponseDTO.model_validate(interest)

    async def update_interest(self, interest_id: str, interest_data: UpdateInterestRequestDTO) -> InterestResponseDTO:
        """Update an existing interest."""
        interest = await self.db.get(Interest, interest_id)
        if not interest:
            raise NotFoundException("Interest not found")

        # Check if another interest with the same name exists (if name is being updated)
        if interest_data.name and interest_data.name != interest.name:
            result = await self.db.execute(select(Interest).where(Interest.name == interest_data.name))
            existing_interest = result.scalar_one_or_none()
            if existing_interest:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Interest with this name already exists",
                )

        # Update fields that are provided
        if interest_data.name is not None:
            interest.name = interest_data.name
        if interest_data.description is not None:
            interest.description = interest_data.description
        if interest_data.category is not None:
            interest.category = interest_data.category
        if interest_data.is_active is not None:
            interest.is_active = interest_data.is_active

        await self.db.commit()
        await self.db.refresh(interest)

        return InterestResponseDTO.model_validate(interest)

    async def delete_interest(self, interest_id: str) -> Dict[str, str]:
        """Soft delete an interest by setting is_active to False."""
        interest = await self.db.get(Interest, interest_id)
        if not interest:
            raise NotFoundException("Interest not found")

        interest.is_active = False
        await self.db.commit()

        return {"message": "Interest deleted successfully"}

    # Avatar upload functionality
    # @staticmethod
    # async def upload_avatar(current_user: AuthUser, file: UploadFile, db: AsyncSession) -> dict:
    #     """Upload and update user avatar."""
    #     from src.helpers.file_upload import FileUploadService

    #     # Save the new avatar file
    #     file_path, file_url = await FileUploadService.save_avatar(file, current_user.id)

    #     # Update user avatar in database
    #     user = await UserService.__get_user_by_id(current_user.id, current_user, db)

    #     # Delete old avatar file if it exists
    #     if user.avatar:
    #         FileUploadService.delete_file(user.avatar)

    #     user.avatar = file_path
    #     await self.db.commit()
    #     await self.db.refresh(user)


class UserService:
    """User service"""

    @staticmethod
    def get_service():
        """Get user service"""
        return UserService()

    @staticmethod
    def _is_email_in_whitelist(email: str) -> bool:
        """Check if email is in the whitelist."""
        try:
            # Get the path to the whitelist file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            whitelist_path = os.path.join(current_dir, "..", "data", "user_white_list.json")

            # Read the whitelist file
            with open(whitelist_path, "r", encoding="utf-8") as file:
                whitelist_data = json.load(file)

            # Check if email exists in the whitelist
            for user in whitelist_data:
                if user.get("email", "").lower() == email.lower():
                    return True

            return False
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            # Log the error if needed and return False for security
            print(f"Error reading whitelist: {e}")
            return False

    @staticmethod
    async def me(current_user: AuthUser, db: AsyncSession) -> User:
        """Get a user by ID"""
        return await UserService.__get_user_by_id(current_user.id, current_user, db)

    @staticmethod
    async def get_user_with_relations(current_user: AuthUser, db: AsyncSession) -> User:
        """Get user with all relationships loaded."""
        result = await db.execute(
            select(User)
            .options(selectinload(User.profile), selectinload(User.interests), selectinload(User.professional_area))
            .where(User.id == current_user.id)
        )
        user = result.scalars().first()
        if not user:
            raise NotFoundException(detail="Utilizador não encontrado!")
        return user

    @staticmethod
    async def __get_user_by_id(user_id: str, current_user: AuthUser, db: AsyncSession) -> User:
        """Get a user by username"""
        if user_id != current_user.id and current_user.role != UserRoleEnum.SUPER_ADMIN:
            raise UnauthorizedException(detail="Você não tem permissão para acessar os dados deste utilizador!")
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NotFoundException(detail="Utilizador não encontrado!")
        return user

    @staticmethod
    async def create_user(user_dto: CreateUserRequestDTO, db: AsyncSession) -> User:
        """Create a new user"""
        # Check if email is in whitelist
        if not UserService._is_email_in_whitelist(user_dto.email):
            raise UnauthorizedException(
                "Este email não está autorizado para registro. Entre em contato com o administrador."
            )

        result = await db.execute(select(User).where(User.email == user_dto.email))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um user com este email.")
        result = await db.execute(select(User).where(User.username == user_dto.username))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username já existe.")
        result = await db.execute(select(User).where(User.phone == user_dto.phone))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Numero de telefone já existe.")

        if user_dto.role not in UserRoleEnum._value2member_map_:
            allowed_roles = ", ".join(role.value for role in UserRoleEnum)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role not allowed. Allowed are [{allowed_roles}]."
            )

        new_user = User(**user_dto.model_dump(exclude={"password"}), password=hash_password(user_dto.password))
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def create_user_in_transaction(user_dto: CreateUserRequestDTO, db: AsyncSession) -> User:
        """Create a new user without committing to the database"""
        # Check if email is in whitelist
        if not UserService._is_email_in_whitelist(user_dto.email):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email não está autorizado para registro. Entre em contato com o administrador.",
            )

        result = await db.execute(select(User).where(User.email == user_dto.email))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um user com este email.")
        result = await db.execute(select(User).where(User.username == user_dto.username))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username já existe.")
        result = await db.execute(select(User).where(User.phone == user_dto.phone))
        if result.scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Numero de telefone já existe.")

        if user_dto.role not in UserRoleEnum._value2member_map_:
            allowed_roles = ", ".join(role.value for role in UserRoleEnum)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role not allowed. Allowed are [{allowed_roles}]."
            )

        new_user = User(**user_dto.model_dump(exclude={"password"}), password=hash_password(user_dto.password))
        db.add(new_user)
        # No commit here - will be handled by the transaction
        await db.flush()  # This updates the object with database values but doesn't commit
        return new_user

    @staticmethod
    async def read_user(user_id: str, current_user: AuthUser, db: AsyncSession) -> User:
        """Get a user by ID"""
        return await UserService.__get_user_by_id(user_id, current_user, db)

    @staticmethod
    async def update_user(
        user_id: str, current_user: AuthUser, user_dto: UpdateUserRequestDTO, db: AsyncSession
    ) -> User:
        """Update a user by ID."""
        user = await UserService.__get_user_by_id(user_id, current_user, db)

        for key, value in user_dto.model_dump().items():
            if key == "full_name":
                value = value.upper()
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(user_id: str, current_user: AuthUser, db: AsyncSession):
        """Delete a user by ID."""
        user = await UserService.__get_user_by_id(user_id, current_user, db)
        await db.delete(user)
        await db.commit()

    @staticmethod
    async def get_all_users(filter_param: FilterParams, db: AsyncSession) -> list[User]:
        """Get all users"""
        stmt = select(User).order_by(User.created_at.desc()).limit(filter_param.limit).offset(filter_param.offset)
        result = await db.execute(stmt)
        users = result.scalars().all()
        return list(users)

    @staticmethod
    async def change_password(
        current_user: AuthUser, password_dto: UserChangePasswordRequestDTO, db: AsyncSession
    ) -> None:
        """Change user password."""
        user = await UserService.__get_user_by_id(current_user.id, current_user, db)

        # Verify current password
        if not verify_password(password_dto.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta")

        # Update password
        user.password = hash_password(password_dto.new_password)
        await db.commit()
        await db.refresh(user)

    # Avatar upload functionality
    # @staticmethod
    # async def upload_avatar(current_user: AuthUser, file: UploadFile, db: AsyncSession) -> dict:
    #     """Upload and update user avatar."""
    #     from src.helpers.file_upload import FileUploadService

    #     # Save the new avatar file
    #     file_path, file_url = await FileUploadService.save_avatar(file, current_user.id)

    #     # Update user avatar in database
    #     user = await UserService.__get_user_by_id(current_user.id, current_user, db)

    #     # Delete old avatar file if it exists
    #     if user.avatar:
    #         FileUploadService.delete_file(user.avatar)

    #     user.avatar = file_path
    #     await db.commit()
    #     await db.refresh(user)

    #     return {"message": "Avatar carregado com sucesso", "avatar_url": file_url}

    # Onboarding and Professional Profile Methods
    @staticmethod
    async def complete_onboarding(
        user_id: str, onboarding_data: OnboardingQuestionnaireDTO, db: AsyncSession
    ) -> Dict[str, Any]:
        """Complete user onboarding questionnaire."""
        user = await db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")

        # Validate professional area exists
        professional_area = await db.get(ProfessionalArea, str(onboarding_data.professional_area_id))
        if not professional_area:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area not found")

        # Get interests by IDs
        interest_results = await db.execute(
            select(Interest).where(Interest.id.in_([str(id) for id in onboarding_data.interest_ids]))
        )
        interests = interest_results.scalars().all()

        if len(interests) != len(onboarding_data.interest_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more interest IDs are invalid")

        # Update professional profile fields
        user.professional_area_id = str(onboarding_data.professional_area_id)
        user.organization = onboarding_data.organization
        user.experience_level = onboarding_data.experience_level.value
        user.preferred_interaction_style = onboarding_data.preferred_interaction_style.value

        # Update user interests relationship
        user.interests = interests

        # Store full onboarding data
        onboarding_json = {
            "professional_area_id": str(onboarding_data.professional_area_id),
            "organization": onboarding_data.organization,
            "experience_level": onboarding_data.experience_level.value,
            "interest_ids": [str(id) for id in onboarding_data.interest_ids],
            "preferred_interaction_style": onboarding_data.preferred_interaction_style.value,
            "use_cases": onboarding_data.use_cases,
            "goals": onboarding_data.goals,
            "completed_at": str(datetime.now()),
        }
        user.onboarding_data = json.dumps(onboarding_json)
        user.onboarding_completed = True

        await db.commit()
        await db.refresh(user)

        return {"message": "Onboarding completed successfully", "professional_profile": user.get_professional_profile()}

    @staticmethod
    async def update_professional_profile(
        user_id: str, profile_data: UserProfessionalProfileUpdateDTO, db: AsyncSession
    ) -> Dict[str, Any]:
        """Update user professional profile."""
        user = await db.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")

        # Update fields that are provided
        if profile_data.professional_area_id is not None:
            # Validate professional area exists
            professional_area = await db.get(ProfessionalArea, str(profile_data.professional_area_id))
            if not professional_area:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professional area not found")
            user.professional_area_id = str(profile_data.professional_area_id)
        if profile_data.organization is not None:
            user.organization = profile_data.organization
        if profile_data.experience_level is not None:
            user.experience_level = profile_data.experience_level.value
        if profile_data.interest_ids is not None:
            # Get interests by IDs
            interest_results = await db.execute(
                select(Interest).where(Interest.id.in_([str(id) for id in profile_data.interest_ids]))
            )
            interests = interest_results.scalars().all()

            if len(interests) != len(profile_data.interest_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="One or more interest IDs are invalid"
                )

            user.interests = interests
        if profile_data.preferred_interaction_style is not None:
            user.preferred_interaction_style = profile_data.preferred_interaction_style.value

        await db.commit()
        await db.refresh(user)

        return {
            "message": "Professional profile updated successfully",
            "professional_profile": user.get_professional_profile(),
        }
