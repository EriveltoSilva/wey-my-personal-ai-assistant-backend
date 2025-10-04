"""Test script for chat history and background task functionality."""

import asyncio
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.chats.background_tasks import background_tasks
from src.chats.enums import MessageSenderEnum, MessageTypeEnum


async def test_background_tasks():
    """Test the background task functionality."""
    print("Starting background task test...")

    # Start background processing
    await background_tasks.start_processing()
    print("Background processing started")

    # Queue some test messages
    await background_tasks.queue_message(
        chat_id="test-chat-1",
        user_id="test-user-1",
        content="Hello, this is a test message!",
        sender=MessageSenderEnum.USER,
        message_type=MessageTypeEnum.TEXT,
    )

    await background_tasks.queue_message(
        chat_id="test-chat-1",
        user_id="test-user-1",
        content="This is an AI response.",
        sender=MessageSenderEnum.AGENT,
        message_type=MessageTypeEnum.TEXT,
        tokens_used=50,
        response_time_ms=1500,
        model_used="gpt-3.5-turbo",
        temperature_used=0.7,
    )

    print("Messages queued successfully")

    # Wait a bit for processing
    await asyncio.sleep(2)

    # Stop background processing
    await background_tasks.stop_processing()
    print("Background processing stopped")

    print("Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_background_tasks())
