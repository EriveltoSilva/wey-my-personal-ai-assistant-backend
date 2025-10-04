"""Agent enums for categorization and configuration."""

from enum import Enum


class AgentCategoryEnum(str, Enum):
    """Categories for different agent specializations."""

    MARKETING = "marketing"
    FINANCE = "finance"
    LEGAL = "legal"
    SALES = "sales"
    HR = "hr"
    TECHNOLOGY = "technology"
    CONSULTING = "consulting"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    GENERAL = "general"


class AgentStatusEnum(str, Enum):
    """Status of an agent."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


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


class ToolsEnabledEnum(str, Enum):
    """Tools that can be enabled for agents."""

    WEB_SEARCH = "web_search"
    CALCULATOR = "calculator"
    CODE_INTERPRETER = "code_interpreter"
    DOCUMENT_ANALYSIS = "document_analysis"
    EMAIL_DRAFT = "email_draft"
    PRESENTATION_GENERATOR = "presentation_generator"
    FINANCIAL_ANALYSIS = "financial_analysis"
    LEGAL_RESEARCH = "legal_research"
    MARKET_RESEARCH = "market_research"
