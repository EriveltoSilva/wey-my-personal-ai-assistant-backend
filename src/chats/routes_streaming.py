import asyncio
from datetime import datetime
from typing import Annotated, AsyncIterator

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import AIMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from src.chats.background_tasks import background_tasks
from src.chats.enums import MessageSenderEnum, MessageTypeEnum
from src.chats.prompts import MY_SYSTEM_MESSAGE
from src.chats.schemas_streaming import Conversation, Message
from src.chats.services import ChatService
from src.core.config import settings
from src.core.logger import logger
from src.core.security import auth_user_dependency, db_dependency

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
router = APIRouter(prefix="/chat", tags=["Chat Streaming"])


async def send_message_with_history(
    conversation: Conversation, chat_id: str, user_id: str, db: AsyncSession
) -> AsyncIterator[str]:
    """Send a message with database history integration."""
    start_time = datetime.now()
    callback = AsyncIteratorCallbackHandler()

    # Get chat service
    chat_service = ChatService(db)

    # Get or create chat
    chat = await chat_service.get_chat_by_id(chat_id=chat_id, user_id=user_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Save user message immediately (non-blocking)
    user_message_content = conversation.messages[-1].content
    await background_tasks.queue_message(
        chat_id=chat_id,
        user_id=user_id,
        content=user_message_content,
        sender=MessageSenderEnum.USER,
        message_type=MessageTypeEnum.TEXT,
    )

    model = ChatOpenAI(
        callbacks=[callback],
        api_key=settings.OPENAI_API_KEY,
        model=(
            conversation.model_name
            if conversation.model_name in {settings.OPENAI_DEFAULT_MODEL, "gpt-3.5-turbo", "gpt-4o-mini"}
            else settings.OPENAI_DEFAULT_MODEL
        ),
        verbose=settings.VERBOSE,
        streaming=conversation.streaming_mode,
        temperature=conversation.temperature,
        max_tokens=settings.MESSAGES_MAX_TOKENS,
    )

    messages = [
        (HumanMessage if msg.role == "user" else AIMessage)(content=msg.content)
        for msg in conversation.messages[-settings.MESSAGES_MAX_NUMBER_IN_HISTORIC :]
    ]

    messages.insert(0, MY_SYSTEM_MESSAGE)

    # Start the LLM task
    task = asyncio.create_task(model.agenerate(messages=[messages]))

    # Collect response for database storage
    full_response = ""
    token_count = 0

    try:
        async for token in callback.aiter():
            full_response += token
            token_count += 1

            # Format the token for SSE
            if "\n" in token:
                print(f"(Break line)>{token}", sep="")
                token = token.replace("\n", "<br/>")
            print(token, sep="")

            yield f"data: {token}\n\n"
    except Exception as e:
        logger.error(f"Error during message streaming: {e}")
        yield f"data: [ERROR] {str(e)}\n\n"
    finally:
        callback.done.set()

    # Wait for task completion and calculate metrics
    try:
        await task
        end_time = datetime.now()
        response_time_ms = int((end_time - start_time).total_seconds() * 1000)

        # Queue agent response for database storage (non-blocking)
        if full_response.strip():
            await background_tasks.queue_message(
                chat_id=chat_id,
                user_id=user_id,
                content=full_response,
                sender=MessageSenderEnum.AGENT,
                message_type=MessageTypeEnum.TEXT,
                tokens_used=token_count,
                response_time_ms=response_time_ms,
                model_used=conversation.model_name or settings.OPENAI_DEFAULT_MODEL,
                temperature_used=conversation.temperature,
            )

    except Exception as e:
        logger.error(f"Error in task completion: {e}")
        yield f"data: [TASK_ERROR] {str(e)}\n\n"


@router.post(f"/quick_response", tags=["Chat"])
async def chat_quick_response(message: Message):
    model = ChatOpenAI(
        verbose=settings.VERBOSE, temperature=settings.MESSAGE_RESPONSE_TEMPERATURE, api_key=settings.OPENAI_API_KEY
    )
    response = model.invoke([MY_SYSTEM_MESSAGE, HumanMessage(content=message.content)])
    return {"response": response.content}


@router.post("/conversation/{chat_id}")
async def stream_chat_message(
    chat_id: str, conversation: Annotated[Conversation, Body()], current_user: auth_user_dependency, db: db_dependency
):
    """Stream a chat message with database persistence."""
    logger.info(f"Received message for chat {chat_id}: {conversation.messages[-1].content}")

    generator = send_message_with_history(conversation, chat_id, current_user.id, db)

    return StreamingResponse(
        generator,
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "Access-Control-Allow-Origin": "*"},
    )


@router.get("/history/{chat_id}")
async def get_chat_history(
    chat_id: str, current_user: auth_user_dependency, db: db_dependency, limit: int = 100, offset: int = 0
):
    """Get chat history from database."""
    chat_service = ChatService(db)

    # Verify chat belongs to user
    chat = await chat_service.get_chat_by_id(chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = await chat_service.get_chat_messages(chat_id, limit, offset)

    return {
        "chat_id": chat_id,
        "messages": [
            {
                "id": msg.id,
                "content": msg.content,
                "sender": msg.sender,
                "message_type": msg.message_type,
                "created_at": msg.created_at,
                "tokens_used": msg.tokens_used,
                "response_time_ms": msg.response_time_ms,
            }
            for msg in messages
        ],
    }
