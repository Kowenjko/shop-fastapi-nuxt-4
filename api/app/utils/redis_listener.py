import json
from app.core.ws_manager import ws_manager

from app.core.redis import redis


async def ws_redis_listener():

    pubsub = redis.pubsub()
    await pubsub.subscribe("ws:orders")

    print("🟢 Redis WS listener started")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])
        print("📨 REDIS MESSAGE:", data)
        user_id = int(data.get("user_id"))
        print("👤 TARGET USER:", user_id)

        if user_id:
            await ws_manager.send_to_user(user_id, data)
