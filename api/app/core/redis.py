from redis.asyncio import Redis
from app.core.config import settings

redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db.cache,
    decode_responses=True,
)
