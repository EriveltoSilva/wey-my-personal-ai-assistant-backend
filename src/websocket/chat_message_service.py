"""
WebSocket message processing service.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.websocket.schemas import WebSocketMessageType

logger = logging.getLogger(__name__)


async def process_websocket_message(message_data: Dict[str, Any], user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """
    Process a message received from WebSocket.
    Args:
        message_data: The message data from WebSocket
        user_id: The user ID who sent the message
        db: Database session

    Returns:
        Response message to send back to WebSocket
    """
    try:
        message_type = message_data.get("type")
        data = message_data.get("data", {})

        if message_type == "user_message":
            return await __process_user_message(data, user_id, db)
        elif message_type == "typing":
            return await __process_typing_message(data, user_id)
        elif message_type == "stop_typing":
            return await __process_stop_typing_message(data, user_id)
        else:
            return _create_error_response(f"Unknown message type: {message_type}")

    except Exception as e:
        logger.error(f"Error processing WebSocket message: {str(e)}")
        return _create_error_response(f"Error processing message: {str(e)}")


async def __process_user_message(data: Dict[str, Any], user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Process a user message and generate agent response."""
    try:
        content = data.get("content", "")
        room_id = data.get("roomId", "default-room")
        sender = data.get("sender", "Unknown")

        if not content.strip():
            return _create_error_response("O conteúdo da mensagem não pode estar vazio")

        # Here you would integrate with your AI service
        # For now, we'll create a simple echo response
        agent_response = await __generate_agent_response(content)

        # Create agent response message
        response_message = {
            "type": WebSocketMessageType.AGENT_MESSAGE,
            "data": {
                "id": f"msg_{datetime.now().timestamp()}",
                "content": agent_response,
                "agentId": "ai_assistant",
                "sender": "AI Assistant",
                "roomId": room_id,
                "type": "agent",
                "created_at": datetime.now().isoformat(),
            },
        }

        return response_message

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return _create_error_response(f"Error processing chat message: {str(e)}")


async def __process_typing_message(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Process typing indicator message."""
    return {
        "type": WebSocketMessageType.STATUS,
        "timestamp": datetime.now().isoformat(),
        "data": {"message": "typing_acknowledged", "userId": user_id},
    }


async def __process_stop_typing_message(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Process stop typing indicator message."""
    return {
        "type": WebSocketMessageType.STATUS,
        "timestamp": datetime.now().isoformat(),
        "data": {"message": "stop_typing_acknowledged", "userId": user_id},
    }


async def __generate_agent_response(user_message: str) -> str:
    """
    Generate agent response to user message.
    This is a placeholder - replace with your actual AI service integration.
    """
    # Simple response logic - replace with your AI service
    message_lower = user_message.lower()

    if "olá" in message_lower or "oi" in message_lower or "hello" in message_lower:
        return "Olá! Como posso ajudá-lo hoje?"
    elif "como está" in message_lower or "how are you" in message_lower:
        return "Estou bem, obrigado por perguntar! Como posso ajudá-lo?"
    elif "obrigado" in message_lower or "thank you" in message_lower:
        return "De nada! Fico feliz em poder ajudar."
    elif "ajuda" in message_lower or "help" in message_lower:
        return "Claro! Estou aqui para ajudar. Pode me fazer qualquer pergunta ou pedir assistência."
    else:
        return f"Recebi sua mensagem: '{user_message}'. Como posso ajudá-lo com isso?"


def _create_error_response(error_message: str) -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        "type": WebSocketMessageType.ERROR,
        "timestamp": datetime.now().isoformat(),
        "data": {"error": error_message, "message": "An error occurred while processing your request"},
    }
    pass
