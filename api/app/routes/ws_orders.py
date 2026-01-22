# app/routes/ws_orders.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import ws_manager

from app.utils import decode_jwt

router = APIRouter(tags=["Orders WS"])


@router.websocket("")
async def orders_ws(
    websocket: WebSocket,
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    payload = decode_jwt(token)
    user_id = int(payload["sub"])

    await ws_manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, websocket)
