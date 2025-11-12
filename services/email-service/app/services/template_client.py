import httpx
from typing import Optional, Dict
from app.config import settings


async def get_template(template_code: str) -> Optional[Dict]:
    """Fetch template from Template Service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.template_service_url}/api/v1/templates/{template_code}",
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("data")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch template: {e}")
        return None


async def render_template(template_code: str, variables: Dict[str, str]) -> Optional[Dict]:
    """Render template with variables"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.template_service_url}/api/v1/templates/{template_code}/render",
                json={"variables": variables},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("data")
            return None
    except Exception as e:
        print(f"❌ Failed to render template: {e}")
        return None
