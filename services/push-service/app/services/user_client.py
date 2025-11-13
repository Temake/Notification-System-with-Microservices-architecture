import httpx
from typing import Optional, Dict
from app.config import settings


async def get_user(user_id: str) -> Optional[Dict]:
    """Fetch user from User Service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.user_service_url}/api/v1/users/{user_id}",
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("data")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch user: {e}")
        return None
