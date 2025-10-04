"""Chat enums."""

from enum import Enum


class ChatStatusEnum(str, Enum):
    """Status of a chat session."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MessageSenderEnum(str, Enum):
    """Sender of a message.
    USER: for 'user' messages
    AGENT: for 'agent' messages
    SYSTEM: for 'system' messages
    """

    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class MessageTypeEnum(str, Enum):
    """Type of message.
    TEXT: for 'text' messages
    IMAGE: for 'image' messages
    FILE: for 'file' messages
    CODE: for 'code' messages
    SYSTEM_INFO: for information about system
    ERROR: for 'error' messages
    """

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    CODE = "code"
    SYSTEM_INFO = "system_info"
    ERROR = "error"
