from fastapi import WebSocket
from typing import Dict, Set


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, set()).add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_to_user(self, user_id: int, message: dict):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_json(message)

    async def broadcast(self, message: dict):
        for sockets in self.active_connections.values():
            for ws in sockets:
                await ws.send_json(message)


ws_manager = WebSocketManager()
