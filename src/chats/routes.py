"""Chat routes for API endpoints."""

from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, Query, status
from src.chats.models import ChatMessage
from src.chats.routes_streaming import chat_quick_response
from src.chats.schemas import ChatCreate, ChatMessageResponse, ChatResponse, MessageSenderEnum, MessageTypeEnum
from src.chats.schemas_streaming import Message
from src.chats.services import ChatService
from src.core.config import settings
from src.core.logger import logger
from src.core.schemas import FilterParams
from src.core.security import auth_user_dependency, db_dependency
from src.exceptions import NotFoundException

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: ChatCreate, current_user: auth_user_dependency, db: db_dependency):
    """Create a new chat."""
    try:
        chat_service = ChatService(db)
        start_time = datetime.now()

        # Create the chat with initial user message
        chat = await chat_service.create_chat(user_id=str(current_user.id), chat_data=chat_data)

        try:
            message = Message(role=MessageSenderEnum.USER.value, content=chat_data.initial_message)
            ai_response = await chat_quick_response(message)

            if ai_response and ai_response.get("response"):
                # Calculate response time
                response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                ai_message = ChatMessage(
                    chat_id=chat.id,
                    content=ai_response["response"],
                    sender=MessageSenderEnum.AGENT,
                    message_type=MessageTypeEnum.TEXT,
                    tokens_used=0,  # TODO: Implement token counting
                    response_time_ms=response_time_ms,
                    model_used=settings.OPENAI_DEFAULT_MODEL,
                    temperature_used=settings.MESSAGE_RESPONSE_TEMPERATURE,
                )

                message_response = db.add(ai_message)
                await db.commit()
                await db.refresh(ai_message)

                chat.message_count += 1
                chat.last_message_at = datetime.now()
                chat.total_tokens_used += 0  # TODO: Add actual token count when available
                await db.commit()

        except Exception as ai_error:
            logger.error(f"Failed to generate AI response for chat {chat.id}: {ai_error}")

        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
async def get_user_chats(
    params: Annotated[FilterParams, Query()], current_user: auth_user_dependency, db: db_dependency
):
    """Get user's recent chats."""
    try:
        chat_service = ChatService(db)
        chats = await chat_service.get_recent_chats_for_user(user_id=current_user.id, params=params)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chat_id}", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def get_chat(chat_id: Annotated[str, Path()], current_user: auth_user_dependency, db: db_dependency):
    """Get a specific chat."""

    try:
        chat_service = ChatService(db)
        chat = await chat_service.get_chat_by_id(chat_id, user_id=current_user.id)
        if not chat:
            raise NotFoundException("Ups! Chat não encontrado!")
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: str, current_user: auth_user_dependency, db: db_dependency):
    """Delete a chat."""
    chat_service = ChatService(db)

    try:
        success = await chat_service.delete_chat(chat_id, user_id=current_user.id)
        if not success:
            raise NotFoundException("Ups! Chat não encontrado!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Handle Archived Chats
@router.get("/me/archived", response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
async def list_user_archived_chats(
    params: Annotated[FilterParams, Query()], current_user: auth_user_dependency, db: db_dependency
):
    """Get user's archived chats."""
    try:
        chat_service = ChatService(db)
        chats = await chat_service.get_archived_chats_for_user(user_id=current_user.id, params=params)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{chat_id}/archive", response_model=ChatResponse)
async def archive_chat(chat_id: Annotated[str, Path()], current_user: auth_user_dependency, db: db_dependency):
    """Archive a chat."""
    try:
        chat_service = ChatService(db)
        chat = await chat_service.archive_chat(chat_id, user_id=current_user.id)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{chat_id}/unarchive", response_model=ChatResponse)
async def unarchive_chat(chat_id: Annotated[str, Path()], current_user: auth_user_dependency, db: db_dependency):
    """Unarchive a chat."""
    try:
        chat_service = ChatService(db)
        chat = await chat_service.unarchive_chat(chat_id, user_id=current_user.id)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chat_id}/messages", response_model=List[ChatMessageResponse], status_code=status.HTTP_200_OK)
async def get_chat_messages(
    chat_id: Annotated[str, Path()],
    params: Annotated[FilterParams, Query()],
    current_user: auth_user_dependency,
    db: db_dependency,
):
    """Get messages for a specific chat."""
    try:
        chat_service = ChatService(db)
        messages = await chat_service.get_chat_messages(chat_id, params=params)
        return [
            ChatMessageResponse(
                id=msg.id,
                content=msg.content,
                role=msg.sender,
                message_type=msg.message_type,
                created_at=msg.created_at,
                tokens_used=msg.tokens_used,
                response_time_ms=msg.response_time_ms,
                model_used=msg.model_used,
            )
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
