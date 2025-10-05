"""Chat services for business logic and AI integration."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.chats.enums import ChatStatusEnum, MessageSenderEnum, MessageTypeEnum
from src.chats.models import Chat, ChatMessage
from src.chats.schemas import ChatCreate
from src.core.schemas import FilterParams
from src.exceptions import NotFoundException


class ChatService:
    """Service for managing chats and messages."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, user_id: str, chat_data: ChatCreate) -> Chat:
        """Create a new chat."""
        new_chat = Chat(
            user_id=user_id,
            title=Chat.generate_title(chat_data.initial_message),
            status=ChatStatusEnum.ACTIVE.value,
            last_message_at=datetime.now(),
        )

        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)

        new_chat_message = ChatMessage(
            chat_id=new_chat.id,
            content=chat_data.initial_message,
            sender=MessageSenderEnum.USER.value,
            message_type=MessageTypeEnum.TEXT.value,
            response_time_ms=0,
            model_used="",
            tokens_used=0,
            temperature_used=0,
        )

        self.db.add(new_chat_message)
        await self.db.commit()
        await self.db.refresh(new_chat_message)

        return new_chat

    async def get_chat_by_id(self, chat_id: str, user_id: str, include_messages: bool = False) -> Optional[Chat]:
        """Get chat by ID."""
        query = select(Chat).where(Chat.id == chat_id)
        query = query.where(Chat.user_id == user_id)
        query = query.where(Chat.status == ChatStatusEnum.ACTIVE.value)

        if include_messages:
            query = query.options(selectinload(Chat.messages))

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_archived_chat_by_id(
        self, chat_id: str, user_id: str, include_messages: bool = False
    ) -> Optional[Chat]:
        """Get archived chat by ID."""
        query = select(Chat).where(Chat.id == chat_id)
        query = query.where(Chat.user_id == user_id)
        query = query.where(Chat.status == ChatStatusEnum.ARCHIVED.value)

        if include_messages:
            query = query.options(selectinload(Chat.messages))

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_recent_chats_for_user(self, user_id: str, params: FilterParams) -> List[Chat]:
        """Get user's most recent chats."""
        query = (
            select(Chat)
            .where(and_(Chat.user_id == user_id, Chat.status != ChatStatusEnum.DELETED.value))
            .order_by(desc(Chat.last_message_at))
            .limit(params.limit)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_archived_chats_for_user(self, user_id: str, params: FilterParams) -> List[Chat]:
        """Get user's archived chats."""
        query = (
            select(Chat)
            .where(and_(Chat.user_id == user_id, Chat.status == ChatStatusEnum.ARCHIVED.value))
            .order_by(desc(Chat.last_message_at))
            .limit(params.limit)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_chat(self, chat_id: str, user_id: Optional[str] = None) -> bool:
        """Delete a chat (soft delete)."""
        chat = await self.get_chat_by_id(chat_id, user_id=user_id)
        if not chat:
            raise NotFoundException(f"Chat with id {chat_id} not found")

        chat.status = ChatStatusEnum.DELETED.value
        await self.db.commit()
        return True

    async def archive_chat(self, chat_id: str, user_id: Optional[str] = None) -> Chat:
        """Archive a chat."""
        chat = await self.get_chat_by_id(chat_id, user_id=user_id)
        if not chat:
            raise NotFoundException(f"Chat with id {chat_id} not found")

        chat.archive()
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def unarchive_chat(self, chat_id: str, user_id: Optional[str] = None) -> Chat:
        """Unarchive a chat."""
        chat = await self.get_archived_chat_by_id(chat_id, user_id=user_id)
        if not chat:
            raise NotFoundException(f"Chat with id {chat_id} not found")

        chat.unarchive()
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    def _generate_title_from_message(self, message: str) -> str:
        """Generate a chat title from the first message."""
        words = message.strip().split()
        if len(words) <= 6:
            return message.strip()

        title = " ".join(words[:6])
        if len(title) > 50:
            title = title[:47] + "..."
        return title

    async def pin_chat(self, chat_id: str, pin: bool, user_id: Optional[str] = None) -> Chat:
        """Pin or unpin a chat."""
        chat = await self.get_chat_by_id(chat_id, user_id=user_id)
        if not chat:
            raise NotFoundException(f"Chat with id {chat_id} not found")

        chat.is_pinned = pin
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    ###############################################################################################
    async def create_or_get_chat(self, user_id: str, title: Optional[str] = None) -> Chat:
        """Create new chat or get existing active chat."""
        # Try to find an existing active chat
        query = (
            select(Chat)
            .where(and_(Chat.user_id == user_id, Chat.status == ChatStatusEnum.ACTIVE.value))
            .order_by(desc(Chat.last_message_at))
            .limit(1)
        )

        result = await self.db.execute(query)
        existing_chat = result.scalars().first()

        if existing_chat:
            return existing_chat

        # Create new chat
        new_chat = Chat(user_id=user_id, title=title or "New Chat", status=ChatStatusEnum.ACTIVE.value)

        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)
        return new_chat

    async def add_message_async(
        self,
        chat_id: str,
        user_id: str,
        content: str,
        sender: MessageSenderEnum,
        message_type: MessageTypeEnum = MessageTypeEnum.TEXT,
        tokens_used: int = 0,
        response_time_ms: Optional[int] = None,
        model_used: Optional[str] = None,
        temperature_used: Optional[float] = None,
    ) -> ChatMessage:
        """Add message to chat asynchronously."""
        message = ChatMessage(
            chat_id=chat_id,
            content=content,
            sender=sender,
            message_type=message_type,
            tokens_used=tokens_used,
            response_time_ms=response_time_ms,
            model_used=model_used,
            temperature_used=temperature_used,
        )

        self.db.add(message)

        # Update chat metrics
        chat = await self.get_chat_by_id(chat_id, user_id=user_id)
        if chat:
            chat.message_count += 1
            chat.last_message_at = datetime.now()
            chat.total_tokens_used += tokens_used

            # Generate title from first user message
            if chat.message_count == 1 and sender == MessageSenderEnum.USER:
                chat.title = Chat.generate_title(content)

        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_chat_messages(self, chat_id: str, params: FilterParams) -> List[ChatMessage]:
        """Get chat messages with pagination."""
        query = (
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_at)
            .offset(params.offset)
            .limit(params.limit)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def batch_create_messages(self, messages: List[dict]) -> List[ChatMessage]:
        """Efficiently create multiple messages in batch."""
        message_objects = [ChatMessage(**msg_data) for msg_data in messages]
        self.db.add_all(message_objects)
        await self.db.commit()

        for msg in message_objects:
            await self.db.refresh(msg)

        return message_objects
