from typing import Optional

from pydantic import BaseModel
from src.chats.enums import MessageSenderEnum
from src.core.config import settings


class Message(BaseModel):
    role: MessageSenderEnum
    content: str


class Conversation(BaseModel):
    streaming_mode: Optional[bool] = True
    search_mode: Optional[bool] = False
    model_name: Optional[str] = None
    temperature: Optional[float] = settings.MESSAGE_RESPONSE_TEMPERATURE
    messages: list[Message]
