import asyncio
from functools import wraps


def retry_with_backoff(max_attempts: int = 3, delay: int = 5):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    wait_time = delay * (2 ** attempt)
                    print(f"⚠️ Retry attempt {attempt + 1}/{max_attempts} after {wait_time}s")
                    await asyncio.sleep(wait_time)
        return wrapper
    return decorator
