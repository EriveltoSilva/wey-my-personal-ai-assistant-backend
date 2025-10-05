"""Chat models."""

import json
import secrets
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.chats.enums import ChatStatusEnum, MessageSenderEnum, MessageTypeEnum
from src.core.database import Base


class Chat(Base):
    """Model for chat sessions between users and agents."""

    __tablename__ = "tbl_chats"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=True)

    # Chat metadata
    status: Mapped[ChatStatusEnum] = mapped_column(String(20), nullable=False, default=ChatStatusEnum.ACTIVE.value)
    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_message_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Context and settings
    context_summary: Mapped[str] = mapped_column(Text, nullable=True)  # AI-generated summary of conversation
    user_preferences: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string of user preferences for this chat

    # User experience
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_shared: Mapped[bool] = mapped_column(Boolean, default=False)
    share_token: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)

    # Metrics
    total_tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    session_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_rating: Mapped[int] = mapped_column(Integer, nullable=True)  # 1-5 rating
    user_feedback: Mapped[str] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    if TYPE_CHECKING:
        from src.users.models import User

    # Relationships
    user_id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="chats")
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="chat", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )

    def __repr__(self):
        return f"<Chat(id={self.id}, title={self.title}, user_id={self.user_id}, status={self.status})>"

    @staticmethod
    def generate_title(first_message: str) -> str:
        """Generate a title based on the first message."""
        # Simple title generation - in production, you might use AI for this
        words = first_message.strip().split()
        if len(words) <= 6:
            return first_message.strip()

        title = " ".join(words[:6])
        if len(title) > 50:
            title = title[:47] + "..."
        return title

    def get_context_for_ai(self, limit: int = 10) -> List[dict]:
        """Get recent messages formatted for AI context."""
        recent_messages = self.messages[-limit:] if len(self.messages) > limit else self.messages

        context = []
        for message in recent_messages:
            context.append(
                {
                    "role": "user" if message.sender == MessageSenderEnum.USER.value else "assistant",
                    "content": message.content,
                }
            )

        return context

    def update_metrics(self, tokens_used: int = 0, duration_minutes: int = 0):
        """Update chat metrics."""
        self.total_tokens_used += tokens_used
        self.session_duration_minutes += duration_minutes
        self.last_message_at = datetime.now()
        self.message_count = len(self.messages)

    def archive(self):
        """Archive the chat."""
        self.status = ChatStatusEnum.ARCHIVED.value

    def unarchive(self):
        """Unarchive the chat."""
        self.status = ChatStatusEnum.ACTIVE.value

    def generate_share_token(self) -> str:
        """Generate a unique share token for the chat."""
        self.share_token = secrets.token_urlsafe(32)
        self.is_shared = True
        return self.share_token


class ChatMessage(Base):
    """Model for individual messages in a chat."""

    __tablename__ = "tbl_chat_messages"

    id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    # Message content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sender: Mapped[MessageSenderEnum] = mapped_column(String(20), nullable=False, index=True)  # user, agent, system
    message_type: Mapped[MessageTypeEnum] = mapped_column(
        String(20), nullable=False, default=MessageTypeEnum.TEXT.value
    )

    # Metadata
    message_metadata: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string for additional data
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)  # Time taken to generate response

    # User feedback
    is_helpful: Mapped[bool] = mapped_column(Boolean, default=True)  # User feedback on message
    user_feedback: Mapped[str] = mapped_column(Text, nullable=True)

    # Processing info
    model_used: Mapped[str] = mapped_column(String(50), nullable=True)  # Which AI model was used
    temperature_used: Mapped[float] = mapped_column(nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    chat_id: Mapped[str] = mapped_column(pg.UUID(as_uuid=True), ForeignKey("tbl_chats.id"), nullable=False, index=True)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    # Add composite indexes for efficient queries
    __table_args__ = (
        Index("idx_chat_messages_chat_created", "chat_id", "created_at"),
        Index("idx_chat_messages_sender_created", "sender", "created_at"),
    )

    def __repr__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, chat_id={self.chat_id}, sender={self.sender}, content='{content_preview}')>"

    def get_metadata_dict(self) -> dict:
        """Get metadata as dictionary."""
        if not self.message_metadata:
            return {}
        try:
            return json.loads(self.message_metadata)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_metadata_dict(self, metadata: dict):
        """Set metadata from dictionary."""
        self.message_metadata = json.dumps(metadata) if metadata else None

    def is_from_user(self) -> bool:
        """Check if message is from user."""
        return self.sender == MessageSenderEnum.USER.value

    def is_from_agent(self) -> bool:
        """Check if message is from agent."""
        return self.sender == MessageSenderEnum.AGENT.value

    def is_from_system(self) -> bool:
        """Check if message is from system."""
        return self.sender == MessageSenderEnum.SYSTEM.value
