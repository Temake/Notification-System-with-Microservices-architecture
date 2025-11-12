import redis.asyncio as redis
import json
from typing import Optional
from app.config import settings

# Redis client
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


async def cache_template(template_code: str, data: dict, ttl: int = 3600):
    """Cache template data"""
    client = await get_redis()
    key = f"template:{template_code}"
    await client.setex(key, ttl, json.dumps(data))


async def get_cached_template(template_code: str) -> Optional[dict]:
    """Get cached template"""
    client = await get_redis()
    key = f"template:{template_code}"
    data = await client.get(key)
    return json.loads(data) if data else None


async def invalidate_cache(template_code: str):
    """Invalidate cached template"""
    client = await get_redis()
    key = f"template:{template_code}"
    await client.delete(key)
