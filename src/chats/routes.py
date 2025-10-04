"""Chat routes for API endpoints."""

from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, Query, status
from src.chats.schemas import ChatCreate, ChatMessageResponse, ChatResponse
from src.chats.services import ChatService
from src.core.schemas import FilterParams
from src.core.security import auth_user_dependency, db_dependency
from src.exceptions import NotFoundException

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: ChatCreate, current_user: auth_user_dependency, db: db_dependency):
    """Create a new chat."""
    try:
        chat_service = ChatService(db)
        chat = await chat_service.create_chat(user_id=str(current_user.id), chat_data=chat_data)
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
