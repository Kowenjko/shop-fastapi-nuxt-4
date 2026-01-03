# app/routes/ws_orders.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import ws_manager

# from app.core.security import decode_jwt

router = APIRouter(tags=["Orders WS"])


@router.websocket("")
async def orders_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    # todo
    # payload = decode_jwt(token)
    # user_id = payload["sub"]

    await ws_manager.connect(3, websocket)

    try:
        while True:
            # можно принимать сообщения от клиента
            data = await websocket.receive_json()
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        # todo
        # ws_manager.disconnect(user_id, websocket)
        ws_manager.disconnect(3, websocket)
