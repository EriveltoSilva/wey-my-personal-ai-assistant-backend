import uuid
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from src.users.enums import ExperienceLevelEnum, InteractionStyleEnum

# from src.general.schemas import AddressResponseDTO, PhoneResponseDTO


# Professional Area Schemas
class CreateProfessionalAreaRequestDTO(BaseModel):
    """Data Transfer Object for creating a professional area."""

    name: str = Field(max_length=100, description="Name of the professional area")
    description: Optional[str] = Field(None, description="Description of the professional area")
    code: Optional[str] = Field(None, max_length=20, description="Short code for the professional area")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Software Development",
                "description": "Software engineering and programming",
                "code": "DEV",
            }
        },
    )


class UpdateProfessionalAreaRequestDTO(BaseModel):
    """Data Transfer Object for updating a professional area."""

    name: Optional[str] = Field(None, max_length=100, description="Name of the professional area")
    description: Optional[str] = Field(None, description="Description of the professional area")
    code: Optional[str] = Field(None, max_length=20, description="Short code for the professional area")
    is_active: Optional[bool] = Field(None, description="Is the professional area active")

    model_config = ConfigDict(from_attributes=True)


class ProfessionalAreaResponseDTO(BaseModel):
    """Data Transfer Object for professional area response."""

    id: uuid.UUID = Field(description="Unique identifier of the professional area")
    name: str = Field(description="Name of the professional area")
    description: Optional[str] = Field(None, description="Description of the professional area")
    code: Optional[str] = Field(None, description="Short code for the professional area")
    is_active: bool = Field(description="Is the professional area active")
    created_at: datetime = Field(description="Creation date of the professional area")
    updated_at: datetime = Field(description="Last update date of the professional area")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "name": "Software Development",
                "description": "Software engineering and programming",
                "code": "DEV",
                "is_active": True,
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z",
            }
        },
    )


# Interest Schemas
class CreateInterestRequestDTO(BaseModel):
    """Data Transfer Object for creating an interest."""

    name: str = Field(max_length=100, description="Name of the interest")
    description: Optional[str] = Field(None, description="Description of the interest")
    category: Optional[str] = Field(None, max_length=50, description="Category of the interest")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Machine Learning",
                "description": "Artificial intelligence and machine learning technologies",
                "category": "technology",
            }
        },
    )


class UpdateInterestRequestDTO(BaseModel):
    """Data Transfer Object for updating an interest."""

    name: Optional[str] = Field(None, max_length=100, description="Name of the interest")
    description: Optional[str] = Field(None, description="Description of the interest")
    category: Optional[str] = Field(None, max_length=50, description="Category of the interest")
    is_active: Optional[bool] = Field(None, description="Is the interest active")

    model_config = ConfigDict(from_attributes=True)


class InterestResponseDTO(BaseModel):
    """Data Transfer Object for interest response."""

    id: uuid.UUID = Field(description="Unique identifier of the interest")
    name: str = Field(description="Name of the interest")
    description: Optional[str] = Field(None, description="Description of the interest")
    category: Optional[str] = Field(None, description="Category of the interest")
    is_active: bool = Field(description="Is the interest active")
    created_at: datetime = Field(description="Creation date of the interest")
    updated_at: datetime = Field(description="Last update date of the interest")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "name": "Machine Learning",
                "description": "Artificial intelligence and machine learning technologies",
                "category": "technology",
                "is_active": True,
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z",
            }
        },
    )


class UserChangePasswordRequestDTO(BaseModel):
    password: str = Field(min_length=8, description="Current password of the user")
    new_password: str = Field(min_length=8, description="New password of the user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "password": "JohnDoe123",
                "new_password": "NewJohnDoe456",
            }
        },
    )


# Profile Schemas
class CreateProfileRequestDTO(BaseModel):
    """Data Transfer Object for creating a user profile."""

    bio: Optional[str] = Field(None, description="User biography")
    gender: Optional[str] = Field(None, max_length=10, description="User gender (MALE/FEMALE/OTHER)")
    birthday: Optional[date] = Field(None, description="User birthday")
    bi: Optional[str] = Field(None, max_length=14, description="Angolan identity document number")
    is_national: bool = Field(default=True, description="Is the user a national citizen")
    passport_number: Optional[str] = Field(None, max_length=20, description="Passport number for non-nationals")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "bio": "Agricultor experiente com foco em cultivos sustentáveis",
                "gender": "MALE",
                "birthday": "1985-03-15",
                "bi": "123456789LA012",
                "is_national": True,
                "passport_number": None,
            }
        },
    )


class UpdateProfileRequestDTO(BaseModel):
    """Data Transfer Object for updating a user profile."""

    bio: Optional[str] = Field(None, description="User biography")
    gender: Optional[str] = Field(None, max_length=10, description="User gender (MALE/FEMALE/OTHER)")
    birthday: Optional[date] = Field(None, description="User birthday")
    bi: Optional[str] = Field(None, max_length=14, description="Angolan identity document number")
    is_national: Optional[bool] = Field(None, description="Is the user a national citizen")
    passport_number: Optional[str] = Field(None, max_length=20, description="Passport number for non-nationals")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "bio": "Agricultor experiente com foco em cultivos sustentáveis",
                "gender": "MALE",
                "birthday": "1985-03-15",
                "bi": "123456789LA012",
                "is_national": True,
                "passport_number": None,
            }
        },
    )


class ProfileResponseDTO(BaseModel):
    """Data Transfer Object for profile response."""

    id: uuid.UUID = Field(description="Unique identifier of the profile")
    bio: Optional[str] = Field(None, description="User biography")
    gender: Optional[str] = Field(None, description="User gender")
    birthday: Optional[date] = Field(None, description="User birthday")
    bi: Optional[str] = Field(None, description="Angolan identity document number")
    is_national: bool = Field(description="Is the user a national citizen")
    passport_number: Optional[str] = Field(None, description="Passport number for non-nationals")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    user_id: uuid.UUID = Field(description="Associated user ID")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "bio": "Agricultor experiente com foco em cultivos sustentáveis",
                "gender": "MALE",
                "birthday": "1985-03-15",
                "bi": "123456789LA012",
                "is_national": True,
                "passport_number": None,
                "photo_url": "https://example.com/photos/profile.jpg",
                "user_id": "67820755-6296-46ae-9193-0c8882050905",
            }
        },
    )


class ProfileWithPhonesResponseDTO(BaseModel):
    """Data Transfer Object for profile response with phones."""

    id: uuid.UUID = Field(description="Unique identifier of the profile")
    bio: Optional[str] = Field(None, description="User biography")
    gender: Optional[str] = Field(None, description="User gender")
    birthday: Optional[date] = Field(None, description="User birthday")
    bi: Optional[str] = Field(None, description="Angolan identity document number")
    is_national: bool = Field(description="Is the user a national citizen")
    passport_number: Optional[str] = Field(None, description="Passport number for non-nationals")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    user_id: uuid.UUID = Field(description="Associated user ID")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "bio": "Agricultor experiente com foco em cultivos sustentáveis",
                "gender": "MALE",
                "birthday": "1985-03-15",
                "bi": "123456789LA012",
                "is_national": True,
                "passport_number": None,
                "photo_url": "https://example.com/photos/profile.jpg",
                "user_id": "67820755-6296-46ae-9193-0c8882050905",
                "phones": [
                    {
                        "id": "67820755-6296-46ae-9193-0c8882050905",
                        "number": "940123456",
                        "profile_id": "67820755-6296-46ae-9193-0c8882050905",
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-01T12:00:00Z",
                    }
                ],
            }
        },
    )


# Avatar Upload Schema
class AvatarUploadResponseDTO(BaseModel):
    """Data Transfer Object for avatar upload response."""

    message: str = Field(description="Success message")
    avatar_url: str = Field(description="URL of the uploaded avatar")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Avatar uploaded successfully",
                "avatar_url": "https://example.com/avatars/user123.jpg",
            }
        },
    )


# Enhanced User Response with nested relationships
class UserWithRelationsResponseDTO(BaseModel):
    """Data Transfer Object for user response with nested relationships."""

    id: Optional[uuid.UUID] = Field(description="Unique identifier of the user")
    full_name: str = Field(max_length=100, description="Full name of the user")
    email: str = Field(description="Email of the user")
    username: str = Field(max_length=30, description="Username of the user")
    phone: str = Field(max_length=13, description="Phone number of the user")
    role: str = Field(description="Role of the user")
    avatar: Optional[str] = Field(description="User avatar URL", default=None)
    is_active: bool = Field(description="Is the user active?")
    is_verified: bool = Field(description="Is the user verified?")
    created_at: Optional[datetime] = Field(description="Creation date of the user")
    updated_at: Optional[datetime] = Field(description="Last update date of the user")

    # Professional fields
    organization: Optional[str] = Field(None, description="User's organization")
    experience_level: Optional[str] = Field(None, description="User's experience level")
    preferred_interaction_style: Optional[str] = Field(None, description="User's preferred interaction style")
    onboarding_completed: bool = Field(description="Has the user completed onboarding")

    # Nested relationships
    profile: Optional[ProfileWithPhonesResponseDTO] = Field(None, description="User profile with phones")
    interests: Optional[List[InterestResponseDTO]] = Field(None, description="User's interests")
    professional_area: Optional[ProfessionalAreaResponseDTO] = Field(None, description="User's professional area")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "phone": "940000000",
                "role": "USER",
                "avatar": "https://example.com/avatars/user123.jpg",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z",
                "organization": "ABC Law Firm",
                "experience_level": "intermediate",
                "preferred_interaction_style": "formal",
                "onboarding_completed": True,
                "professional_area": {
                    "id": "67820755-6296-46ae-9193-0c8882050905",
                    "name": "Legal Practice",
                    "description": "Legal services and law practice",
                    "code": "LAW",
                    "is_active": True,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                },
                "profile": {
                    "id": "67820755-6296-46ae-9193-0c8882050905",
                    "bio": "Agricultor experiente",
                    "gender": "MALE",
                    "birthday": "1985-03-15",
                    "bi": "123456789LA012",
                    "is_national": True,
                    "passport_number": None,
                    "photo_url": "https://example.com/photos/profile.jpg",
                    "user_id": "67820755-6296-46ae-9193-0c8882050905",
                },
                "interests": [
                    {
                        "id": "67820755-6296-46ae-9193-0c8882050905",
                        "name": "Legal Research",
                        "description": "Research in legal documents and case law",
                        "category": "legal",
                        "is_active": True,
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-01T12:00:00Z",
                    }
                ],
            }
        },
    )


class UpdateUserRequestDTO(BaseModel):
    """Data Transfer Object for updating a user."""

    full_name: str = Field(max_length=100, description="Full name of the user")
    username: str = Field(max_length=30, description="Username of the user")
    email: EmailStr
    phone: str = Field(max_length=13, description="Phone number of the user")
    role: str = Field(description="Role of the user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "phone": "940000000",
                "role": "agricultor",
            }
        },
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()


class CreateUserRequestDTO(BaseModel):
    """Data Transfer Object for creating a user."""

    full_name: str = Field(max_length=100, description="Full name of the user")
    username: str = Field(max_length=30, description="Username of the user")
    email: EmailStr
    phone: str = Field(max_length=13, description="Phone number of the user")
    role: str = Field(description="Role of the user")
    password: str = Field(min_length=8, max_length=32, description="Password of the user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "phone": "940000000",
                "role": "agricultor",
                "password": "password123",
            }
        },
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()


class UserResponseDTO(BaseModel):
    """Data Transfer Object for user public response."""

    id: Optional[uuid.UUID] = Field(description="Unique identifier of the user")
    full_name: str = Field(max_length=100, description="Full name of the user")
    email: str = Field(description="Email of the user")
    username: str = Field(max_length=30, description="Username of the user")
    phone: str = Field(max_length=13, description="Phone number of the user")
    role: str = Field(description="Role of the user")
    avatar: Optional[str] = Field(description="User avatar URL", default=None)
    is_active: bool = Field(description="Is the user active?")
    is_verified: bool = Field(description="Is the user verified?")
    created_at: Optional[datetime] = Field(description="Creation date of the user")
    updated_at: Optional[datetime] = Field(description="Last update date of the user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "67820755-6296-46ae-9193-0c8882050905",
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "phone": "940000000",
                "role": "USER",
                "avatar": "https://example.com/avatars/user123.jpg",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-10-01T12:00:00Z",
                "updated_at": "2023-10-01T12:00:00Z",
            }
        },
    )


class OnboardingQuestionnaireDTO(BaseModel):
    """Data Transfer Object for user onboarding questionnaire."""

    professional_area_id: uuid.UUID = Field(..., description="ID of the user's professional area")
    organization: Optional[str] = Field(None, max_length=200, description="User's organization")
    experience_level: ExperienceLevelEnum = Field(..., description="User's experience level")
    interest_ids: List[uuid.UUID] = Field(
        ..., min_items=1, description="List of interest IDs that the user is interested in"
    )
    preferred_interaction_style: InteractionStyleEnum = Field(..., description="Preferred interaction style")
    use_cases: Optional[List[str]] = Field(None, description="Specific use cases for AI agents")
    goals: Optional[str] = Field(None, max_length=1000, description="User's goals with AI agents")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "professional_area_id": "67820755-6296-46ae-9193-0c8882050905",
                "organization": "ABC Law Firm",
                "experience_level": "intermediate",
                "interest_ids": ["67820755-6296-46ae-9193-0c8882050905", "67820755-6296-46ae-9193-0c8882050906"],
                "preferred_interaction_style": "formal",
                "use_cases": ["Legal document review", "Case law research"],
                "goals": "Improve efficiency in legal research and document analysis",
            }
        },
    )


class UserProfessionalProfileUpdateDTO(BaseModel):
    """Data Transfer Object for updating user professional profile."""

    professional_area_id: Optional[uuid.UUID] = None
    organization: Optional[str] = Field(None, max_length=200)
    experience_level: Optional[ExperienceLevelEnum] = None
    interest_ids: Optional[List[uuid.UUID]] = None
    preferred_interaction_style: Optional[InteractionStyleEnum] = None

    model_config = ConfigDict(from_attributes=True)
