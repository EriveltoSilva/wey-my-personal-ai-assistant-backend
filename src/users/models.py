"""User model."""

import uuid
from datetime import date, datetime
from typing import List

from sqlalchemy import Boolean, Column, Date, ForeignKey, String, Table, Text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.agents.enums import ExperienceLevelEnum
from src.agents.models import Agent
from src.chats.models import Chat
from src.core.database import Base
from src.users.enums import GenderEnum, UserRoleEnum

# Association table for many-to-many relationship between User and Interest
user_interest_association = Table(
    "tbl_user_interests",
    Base.metadata,
    Column("user_id", pg.UUID(as_uuid=True), ForeignKey("tbl_users.id"), primary_key=True),
    Column("interest_id", pg.UUID(as_uuid=True), ForeignKey("tbl_interests.id"), primary_key=True),
)


class ProfessionalArea(Base):
    """Model for Professional Areas."""

    __tablename__ = "tbl_professional_areas"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)  # Short code like "LAW", "ENG", "MED"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships - One professional area can have many users
    users: Mapped[List["User"]] = relationship("User", back_populates="professional_area")
    # Many-to-many relationship with agents
    agents: Mapped[List["Agent"]] = relationship(
        "Agent", secondary="tbl_agent_professional_areas", back_populates="professional_areas"
    )

    def __repr__(self):
        return f"<ProfessionalArea(id={self.id}, name={self.name}, code={self.code}, is_active={self.is_active})>"


class Interest(Base):
    """Model for Interest areas."""

    __tablename__ = "tbl_interests"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=True)  # Can be linked to AgentCategoryEnum
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    users: Mapped[List["User"]] = relationship("User", secondary=user_interest_association, back_populates="interests")

    def __repr__(self):
        return f"<Interest(id={self.id}, name={self.name}, category={self.category}, is_active={self.is_active})>"


class User(Base):
    """Model for User."""

    __tablename__ = "tbl_users"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    organization: Mapped[str] = mapped_column(String(200), nullable=True)
    experience_level: Mapped[ExperienceLevelEnum] = mapped_column(String(50), nullable=True)
    preferred_interaction_style: Mapped[str] = mapped_column(String(50), nullable=True)

    # Onboarding status
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    onboarding_data: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string of onboarding responses

    otp: Mapped[str] = mapped_column(String(10), nullable=True)
    role: Mapped[UserRoleEnum] = mapped_column(String(50), nullable=False, default=UserRoleEnum.USER.value)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    # Professional fields for agent matching
    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    professional_area_id: Mapped[str] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("tbl_professional_areas.id"), nullable=True
    )
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    interests: Mapped[List["Interest"]] = relationship(
        "Interest", secondary=user_interest_association, back_populates="users"
    )
    professional_area: Mapped["ProfessionalArea"] = relationship("ProfessionalArea", back_populates="users")

    def __repr__(self):
        return (
            f"<User(id={self.id}, name={self.full_name}, username={self.username}, "
            f"email={self.email}, phone={self.phone}, type={self.role}, is_active={self.is_active}, "
            f"is_verified={self.is_verified})>"
        )

    def get_simple_user_dict(self):
        """Get a simple user dictionary like the one created for the authentication process with get_current_user."""
        return {"id": str(self.id), "username": self.username, "role": self.role, "full_name": self.full_name}

    def get_professional_profile(self):
        """Get user's professional profile for agent matching."""
        return {
            "professional_area": (
                {
                    "id": str(self.professional_area.id),
                    "name": self.professional_area.name,
                    "code": self.professional_area.code,
                }
                if self.professional_area
                else None
            ),
            "organization": self.organization,
            "experience_level": self.experience_level,
            "interests": [interest.name for interest in self.interests] if self.interests else [],
            "preferred_interaction_style": self.preferred_interaction_style,
            "onboarding_completed": self.onboarding_completed,
        }

    def get_accessible_agents_filter(self):
        """Get filter criteria for agents accessible to this user."""
        if not self.onboarding_completed:
            return None

        # Now agents are filtered by professional areas instead of categories
        accessible_professional_areas = []

        # Include user's own professional area
        if self.professional_area:
            accessible_professional_areas.append(
                {
                    "id": str(self.professional_area.id),
                    "name": self.professional_area.name,
                    "code": self.professional_area.code,
                }
            )

        # Add interest-related professional areas if interests map to professional areas
        if self.interests:
            interest_categories = [interest.category for interest in self.interests if interest.category]
            accessible_professional_areas.extend(interest_categories)

        return {
            "professional_areas": accessible_professional_areas,
            "user_professional_area": (
                {
                    "id": str(self.professional_area.id),
                    "name": self.professional_area.name,
                    "code": self.professional_area.code,
                }
                if self.professional_area
                else None
            ),
            "experience_level": self.experience_level,
        }


class Profile(Base):
    """Model for User Profile."""

    __tablename__ = "tbl_profiles"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True, default=GenderEnum.MALE.value)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    bi: Mapped[str] = mapped_column(String(14), nullable=True)
    is_national: Mapped[bool] = mapped_column(Boolean, default=False)
    passport_number: Mapped[str] = mapped_column(String(20), nullable=True)
    photo_url: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    user_id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self):
        return (
            f"<Profile(id={self.id}, gender={self.gender}, birthday={self.birthday}, bi={self.bi}, "
            f"is_national={self.is_national}, passport_number={self.passport_number}, user={self.user.full_name})>"
        )
