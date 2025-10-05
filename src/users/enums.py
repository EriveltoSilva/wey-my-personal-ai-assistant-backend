from enum import Enum


class UserRoleEnum(str, Enum):
    """Enum for user roles."""

    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    AGENT_MANAGER = "agent_manager"  # Can create and manage agents
    USER = "user"
    GUEST = "guest"
    PROFESSIONAL = "professional"


class GenderEnum(str, Enum):
    """Enum for gender."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class ExperienceLevelEnum(str, Enum):
    """Experience levels for users."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class InteractionStyleEnum(str, Enum):
    """Preferred interaction styles."""

    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"
    CONVERSATIONAL = "conversational"
    CONCISE = "concise"
    DETAILED = "detailed"
