"""Agent schemas for API requests and responses."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from src.agents.enums import AgentStatusEnum
from src.core.config import settings
from src.core.schemas import FilterParams


class ProfessionalAreaResponse(BaseModel):
    """Reference to a professional area."""

    id: str
    name: str
    code: Optional[str]
    description: Optional[str]
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        example={
            "id": "65359588-563f-4300-a38a-8df591379a00",
            "name": "Software Development",
            "code": "SWD",
            "description": "Software development and engineering",
            "is_active": True,
        },
    )


# Base schemas
class AgentListParams(FilterParams):
    """Parameters for agent list endpoint."""

    skip: int = Field(default=0, ge=0)
    category: Optional[str] = None
    professional_area_id: Optional[str] = None
    is_featured: Optional[bool] = None
    is_premium: Optional[bool] = None
    search: Optional[str] = None


class AgentCommonResponse(BaseModel):
    """Response schema for agent list."""

    id: str
    name: str
    description: str
    expertise_area: str

    professional_areas: List[ProfessionalAreaResponse] = Field(default_factory=list)

    avatar_url: Optional[str]
    avatar_emoji: str
    primary_color: str

    is_featured: bool
    is_premium: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65359588-563f-4300-a38a-8df591379a00",
                "name": "Software Development",
                "description": "Software engineering and programming",
                "expertise_area": "Software Development",
                "professional_areas": [
                    {"id": "123", "name": "Software Development", "code": "SWD"},
                    {"id": "456", "name": "Artificial Intelligence", "code": "AI"},
                ],
                "avatar_url": "https://github.com/eriveltosilva.png",
                "avatar_emoji": "💻",
                "primary_color": "#3B82F6",
                "usage_count": 100,
                "rating_average": 4.5,
                "rating_count": 10,
                "is_featured": True,
                "is_premium": False,
                "system_prompt": "You are a software development expert.",
                "personality_traits": "Analytical, Detail-oriented",
                "conversation_style": "Formal",
                "tools_enabled": ["code_editor", "debugger"],
                "max_context_length": 4000,
                "temperature": 0.0,
            }
        },
    )


class AgentAdminResponse(AgentCommonResponse):
    """Detailed response schema for single agent."""

    status: AgentStatusEnum

    # Agent personality and behavior
    system_prompt: str
    personality_traits: Optional[str]
    conversation_style: Optional[str]

    # Capabilities and tools
    tools_enabled: List[str]
    max_context_length: int
    temperature: float

    usage_count: int
    rating_average: Optional[float]
    rating_count: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65359588-563f-4300-a38a-8df591379a00",
                "name": "Software Development",
                "description": "Software engineering and programming",
                "expertise_area": "Software Development",
                "professional_areas": [
                    {"id": "123", "name": "Software Development", "code": "SWD"},
                    {"id": "456", "name": "Artificial Intelligence", "code": "AI"},
                ],
                "avatar_url": "https://github.com/eriveltosilva.png",
                "avatar_emoji": "💻",
                "primary_color": "#3B82F6",
                "usage_count": 100,
                "rating_average": 4.5,
                "rating_count": 10,
                "is_featured": True,
                "is_premium": False,
                "system_prompt": "You are a software development expert.",
                "personality_traits": "Analytical, Detail-oriented",
                "conversation_style": "Formal",
                "tools_enabled": ["code_editor", "debugger"],
                "max_context_length": 4000,
                "temperature": 0.0,
                "status": "active",
                "usage_count": 100,
                "rating_average": 4.5,
                "rating_count": 10,
                "system_prompt": "You are a software development expert.",
                "personality_traits": "Analytical, Detail-oriented",
                "conversation_style": "Formal",
                "tools_enabled": ["code_editor", "debugger"],
                "max_context_length": 4000,
                "temperature": 0.0,
            }
        },
    )


class AgentListResponsePaginated(BaseModel):
    """Result schema for paginated agent list."""

    agents: List[AgentCommonResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


# Request schemas


class AgentBase(BaseModel):
    """Base agent schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    expertise_area: str = Field(..., min_length=1, max_length=50)
    professional_area_ids: List[str] = Field(default_factory=list, description="List of professional area IDs")
    system_prompt: str = Field(..., min_length=1)
    personality_traits: Optional[str] = None
    conversation_style: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_emoji: Optional[str] = "🤖"
    primary_color: Optional[str] = "#3B82F6"
    tools_enabled: Optional[List[str]] = None
    max_context_length: int = Field(default=4000, ge=1000, le=32000)
    temperature: float = Field(default=settings.MESSAGE_RESPONSE_TEMPERATURE, ge=0.0, le=2.0)
    is_featured: bool = False
    is_premium: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Software Development",
                "description": "Software engineering and programming",
                "expertise_area": "Software Development",
                "professional_area_ids": ["123", "456"],
                "system_prompt": "You are a software development expert.",
                "personality_traits": "Analytical, Detail-oriented",
                "conversation_style": "Formal",
                "avatar_url": "https://github.com/eriveltosilva.png",
                "avatar_emoji": "💻",
                "primary_color": "#3B82F6",
                "tools_enabled": ["code_editor", "debugger"],
                "max_context_length": 4000,
                "temperature": 0.0,
                "is_featured": True,
                "is_premium": False,
            }
        },
    )


class AgentCreate(AgentBase):
    """Schema for creating a new agent."""

    status: AgentStatusEnum = AgentStatusEnum.ACTIVE

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Software Development",
                "description": "Software engineering and programming",
                "expertise_area": "Software Development",
                "professional_area_ids": ["65359588-563f-4300-a38a-8df591379a00"],
                "system_prompt": "You are a software development expert.",
                "personality_traits": "Analytical, Detail-oriented",
                "conversation_style": "Formal",
                "avatar_url": "https://github.com/eriveltosilva.png",
                "avatar_emoji": "💻",
                "primary_color": "#3B82F6",
                "tools_enabled": ["code_editor", "debugger"],
                "max_context_length": 4000,
                "temperature": 0.0,
                "is_featured": True,
                "is_premium": False,
            }
        },
    )


class AgentUpdate(BaseModel):
    """Schema for updating an agent."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    expertise_area: Optional[str] = Field(None, min_length=1, max_length=50)
    professional_area_ids: Optional[List[str]] = None
    system_prompt: Optional[str] = Field(None, min_length=1)
    personality_traits: Optional[str] = None
    conversation_style: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_emoji: Optional[str] = None
    primary_color: Optional[str] = None
    tools_enabled: Optional[List[str]] = None
    max_context_length: Optional[int] = Field(None, ge=1000, le=32000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    status: Optional[AgentStatusEnum] = None
    is_featured: Optional[bool] = None
    is_premium: Optional[bool] = None


class AgentRating(BaseModel):
    """Schema for rating an agent."""

    rating: float = Field(..., ge=1.0, le=5.0)
    feedback: Optional[str] = Field(None, max_length=1000)
