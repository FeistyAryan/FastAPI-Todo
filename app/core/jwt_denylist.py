import redis.asyncio as redis
from app.core.config import settings
from datetime import datetime, timezone

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def add_jti_to_denylist(jti: str, exp: int):
    time_to_expire = round(exp - datetime.now(timezone.utc).timestamp())
    if time_to_expire > 0:
        await redis_client.setex(jti, time_to_expire, "denied")

async def is_jti_denylisted(jti: str) -> bool:
    return await redis_client.get(jti) is not None

