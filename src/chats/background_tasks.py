"""Background tasks for chat operations."""

import asyncio
from typing import Any, Dict, Optional

from src.chats.enums import MessageSenderEnum, MessageTypeEnum
from src.chats.services import ChatService
from src.core.database import AsyncSessionLocal
from src.core.logger import logger


class ChatBackgroundTasks:
    """Handle background database operations for chat."""

    def __init__(self):
        self.message_queue = asyncio.Queue()
        self.is_processing = False

    async def start_processing(self):
        """Start the background message processing."""
        if self.is_processing:
            return

        self.is_processing = True
        asyncio.create_task(self._process_message_queue())

    async def _process_message_queue(self):
        """Process messages from queue."""
        while self.is_processing:
            try:
                # Get message from queue with timeout
                try:
                    message_data = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                await self._save_message_to_db(message_data)
                self.message_queue.task_done()

            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
                await asyncio.sleep(0.1)

    async def _save_message_to_db(self, message_data: Dict[str, Any]):
        """Save message to database."""
        async with AsyncSessionLocal() as db:
            try:
                chat_service = ChatService(db)
                await chat_service.add_message_async(**message_data)
                logger.debug(f"Message saved to DB: {message_data.get('content', '')[:50]}...")
            except Exception as e:
                logger.error(f"Error saving message to DB: {e}")

    async def queue_message(
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
    ):
        """Queue message for background processing."""
        message_data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "content": content,
            "sender": sender,
            "message_type": message_type,
            "tokens_used": tokens_used,
            "response_time_ms": response_time_ms,
            "model_used": model_used,
            "temperature_used": temperature_used,
        }

        await self.message_queue.put(message_data)

    async def stop_processing(self):
        """Stop background processing."""
        self.is_processing = False

        # Wait for remaining messages to be processed
        await self.message_queue.join()


# Global instance
background_tasks = ChatBackgroundTasks()
