"""Chat schemas for API requests and responses."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator
from src.chats.enums import ChatStatusEnum, MessageSenderEnum, MessageTypeEnum


class ChatCreate(BaseModel):
    """Schema for creating a new chat."""

    initial_message: str

    @field_validator("initial_message")
    def validate_initial_message(cls, value):
        if not value:
            raise ValueError("Mensagem inicial não pode estar vazia")
        return value


class ChatResponse(BaseModel):
    """Schema for chat response."""

    id: UUID
    title: Optional[str]
    status: ChatStatusEnum
    message_count: int
    last_message_at: Optional[datetime]
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    """Schema for chat message response."""

    id: UUID
    content: str
    role: MessageSenderEnum
    message_type: MessageTypeEnum
    created_at: datetime
    tokens_used: int
    response_time_ms: Optional[int]
    model_used: Optional[str]

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response."""

    chat_id: UUID
    messages: list[ChatMessageResponse]
    total_count: Optional[int] = None
