"""Agent models."""

import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.agents.enums import AgentStatusEnum
from src.core.database import Base

# Association table for many-to-many relationship between Agent and ProfessionalArea
agent_professional_area_association = Table(
    "tbl_agent_professional_areas",
    Base.metadata,
    Column("agent_id", pg.UUID(as_uuid=True), ForeignKey("tbl_agents.id"), primary_key=True),
    Column("professional_area_id", pg.UUID(as_uuid=True), ForeignKey("tbl_professional_areas.id"), primary_key=True),
)


class Agent(Base):
    """Model for AI Agents."""

    __tablename__ = "tbl_agents"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    expertise_area: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Agent personality and behavior
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    ## Para remover
    personality_traits: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    conversation_style: Mapped[str] = mapped_column(Text, nullable=True)

    # Visual and branding
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    avatar_emoji: Mapped[str] = mapped_column(String(10), nullable=True, default="🤖")
    primary_color: Mapped[str] = mapped_column(String(7), nullable=True, default="#3B82F6")

    # Capabilities and tools
    tools_enabled: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array of enabled tools
    max_context_length: Mapped[int] = mapped_column(nullable=False, default=4000)
    temperature: Mapped[float] = mapped_column(nullable=False, default=0.7)

    # Usage and performance
    usage_count: Mapped[int] = mapped_column(nullable=False, default=0)
    rating_average: Mapped[float] = mapped_column(nullable=True)
    rating_count: Mapped[int] = mapped_column(nullable=False, default=0)

    # Status and configuration
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=AgentStatusEnum.ACTIVE.value)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from src.chats.models import Chat
        from src.users.models import ProfessionalArea
    # Relationships
    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="agent", cascade="all, delete-orphan")
    examples: Mapped[List["AgentExample"]] = relationship("AgentExample", cascade="all, delete-orphan")
    professional_areas: Mapped[List["ProfessionalArea"]] = relationship(
        "ProfessionalArea", secondary=agent_professional_area_association, back_populates="agents"
    )

    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name}, expertise_area={self.expertise_area}, status={self.status})>"

    def get_agent_professional_areas(self):
        """Get a list of professional areas for the agent."""
        from src.agents.schemas import ProfessionalAreaResponse

        return [
            ProfessionalAreaResponse(
                id=str(area.id), name=area.name, code=area.code, description=area.description, is_active=area.is_active
            )
            for area in self.professional_areas
        ]

    def get_configuration(self):
        """Get agent configuration for AI model."""
        import json

        tools = []
        if self.tools_enabled:
            try:
                tools = json.loads(self.tools_enabled)
            except (json.JSONDecodeError, TypeError):
                tools = []

        return {
            "system_prompt": self.system_prompt,
            "personality_traits": self.personality_traits,
            "conversation_style": self.conversation_style,
            "tools_enabled": tools,
            "max_context_length": self.max_context_length,
            "temperature": self.temperature,
        }

    def get_usage_stats(self):
        """Get agent usage statistics."""
        return {
            "usage_count": self.usage_count,
            "rating_average": self.rating_average,
            "rating_count": self.rating_count,
            "popularity_score": self.usage_count + (self.rating_average or 0) * self.rating_count,
        }

    def increment_usage(self):
        """Increment usage count."""
        self.usage_count += 1

    def update_rating(self, new_rating: float):
        """Update agent rating with new user rating."""
        if self.rating_count == 0:
            self.rating_average = new_rating
        else:
            total_rating = (self.rating_average * self.rating_count) + new_rating
            self.rating_count += 1
            self.rating_average = total_rating / self.rating_count

        if self.rating_count == 0:
            self.rating_count = 1


class AgentExample(Base):
    """Model for Agent example conversations/use cases."""

    __tablename__ = "tbl_agent_examples"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    agent_id: Mapped[str] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("tbl_agents.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    agent_response: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array of tags

    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    order_priority: Mapped[int] = mapped_column(nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<AgentExample(id={self.id}, agent_id={self.agent_id}, title={self.title})>"
