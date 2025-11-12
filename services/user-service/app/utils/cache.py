import redis.asyncio as redis
import json
from typing import Optional
from app.config import settings

redis_client: Optional[redis.Redis] = None


async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password if settings.redis_password else None,
            decode_responses=True
        )
    return redis_client


async def cache_user(user_id: int, data: dict, ttl: int = 3600):
    """Cache user data"""
    client = await get_redis()
    key = f"user:{user_id}"
    await client.setex(key, ttl, json.dumps(data))


async def get_cached_user(user_id: int) -> Optional[dict]:
    """Get cached user"""
    client = await get_redis()
    key = f"user:{user_id}"
    data = await client.get(key)
    return json.loads(data) if data else None


async def invalidate_user_cache(user_id: int):
    """Invalidate cached user"""
    client = await get_redis()
    key = f"user:{user_id}"
    await client.delete(key)
