import logging
from typing import Dict, List

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketConnectionManager:
    def __init__(self):
        # Dictionary to store clients by user_id
        # Structure: {user_id: [websocket1, websocket2, ...]}
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """Accept a new WebSocket connection and register it for a user"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(
            f"WebSocket connected for user {user_id}. Total connections: {len(self.active_connections[user_id])}"
        )

    async def disconnect(self, user_id: str, websocket: WebSocket):
        """Disconnect a WebSocket connection for a user"""
        if user_id in self.active_connections and websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)
            logger.info(
                f"WebSocket disconnected for user {user_id}. Remaining connections: {len(self.active_connections[user_id])}"
            )

            # Clean up empty user entries
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, data: dict) -> bool:
        """Send data to all WebSocket connections for a specific user"""
        if user_id not in self.active_connections or not self.active_connections[user_id]:
            return False

        disconnected = []
        for ws in self.active_connections[user_id]:
            try:
                await ws.send_json(data)
            except Exception as e:
                logger.error(f"Error sending websocket data to user {user_id}: {str(e)}")
                disconnected.append(ws)

        # Clean up disconnected clients
        for ws in disconnected:
            await self.disconnect(user_id, ws)

        return bool(len(self.active_connections.get(user_id, [])) > 0)

    async def broadcast_to_user(self, user_id: str, data: dict) -> bool:
        """Broadcast data to all WebSocket connections for a specific user"""
        if user_id not in self.active_connections or not self.active_connections[user_id]:
            return False

        disconnected = []
        for ws in self.active_connections[user_id]:
            try:
                await ws.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting websocket data to user {user_id}: {str(e)}")
                disconnected.append(ws)

        # Clean up disconnected clients
        for ws in disconnected:
            await self.disconnect(user_id, ws)

        return bool(len(self.active_connections.get(user_id, [])) > 0)

    async def broadcast_to_all(self, data: dict):
        """Broadcast data to all connected clients"""
        users_to_check = list(self.active_connections.keys())

        for user_id in users_to_check:
            await self.send_to_user(user_id, data)


ws_manager = WebSocketConnectionManager()
