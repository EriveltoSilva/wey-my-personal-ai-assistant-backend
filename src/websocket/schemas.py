from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class WebSocketMessageType(str, Enum):
    """Types of WebSocket messages."""

    USER_MESSAGE = "user_message"  # User Message
    AGENT_MESSAGE = "agent_message"  # Agent Message
    TYPING = "typing"  # User is typing
    STOP_TYPING = "stop_typing"  # User stopped typing
    ERROR = "error"  # Error message


class WebSocketMessage(BaseModel):
    """Base model for all WebSocket messages."""

    type: WebSocketMessageType = Field(description="Message type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    data: Dict[str, Any] = Field(description="Message data")


class WebSocketErrorMessage(WebSocketMessage):
    """Model for error messages."""

    type: WebSocketMessageType = WebSocketMessageType.ERROR
    error: str = Field(description="Error description")


# class WebSocketCommandMessage(BaseModel):
#     """Model for device command messages from WebSocket."""

#     type: str = Field(description="Device type (e.g., 'cis')")
#     command: str = Field(description="Command to execute")
#     device_id: str = Field(description="Device MAC address or ID")
#     parameters: Optional[str] = Field(default=None, description="Optional command parameters")

# class WebSocketTelemetryMessage(WebSocketMessage):
#     """Model for device telemetry data messages."""

#     type: WebSocketMessageType = WebSocketMessageType.TELEMETRY
#     device_id: str = Field(description="Device ID that sent the telemetry")
#     device_name: str = Field(description="Device name")
#     # device_type: DeviceType = Field(description="Device type (SNM, WRC, etc.)")
#     farm_id: str = Field(description="Farm ID the device belongs to")
