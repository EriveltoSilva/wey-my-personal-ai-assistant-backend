import json
import logging

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status
from src.core.database import get_db
from src.core.security import verify_token
from src.websocket.chat_message_service import process_websocket_message
from src.websocket.manager import ws_manager
from src.websocket.schemas import WebSocketMessageType

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    # Validate the token and extract user_id
    # logger.info(f"New WebSocket connection attempt ith token: {token}")
    logger.info(f"New WebSocket connection attempt.")
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            logger.error(f"Token credentials invalid, user id does not exist!")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception as e:
        logger.error(f"Invalid token in WebSocket connection: {str(e)}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Register the client with the user_id
    await ws_manager.connect(user_id, websocket)

    try:
        # await websocket.send_json(welcome_message)

        # Keep the connection alive until a disconnect event
        while True:
            # Receive and process incoming messages
            data = await websocket.receive_text()

            logger.info(f"Received data from WebSocket: {data}")
            try:
                # Parse JSON data
                message_data = json.loads(data)

                # Get database session
                db_generator = get_db()
                db = await anext(db_generator)

                try:
                    # Process the command
                    response = await process_websocket_message(message_data, user_id, db)
                    await websocket.send_json(response)
                finally:
                    await db_generator.aclose()

            except json.JSONDecodeError:
                # Handle invalid JSON
                error_response = {"type": WebSocketMessageType.ERROR, "error": "Invalid JSON format", "data": {}}
                await websocket.send_json(error_response)
            except Exception as e:
                # Handle other errors
                logger.error(f"Error processing WebSocket message: {str(e)}")
                error_response = {
                    "type": WebSocketMessageType.ERROR,
                    "error": f"Error processing message: {str(e)}",
                    "data": {},
                }
                await websocket.send_json(error_response)
    except WebSocketDisconnect as e:
        logger.info(f"WebSocket client disconnected: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        logger.exception(e)
    finally:
        # Clean up the connection
        await ws_manager.disconnect(user_id, websocket)
