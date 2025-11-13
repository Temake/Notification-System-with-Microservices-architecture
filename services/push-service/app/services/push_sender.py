import asyncio
import httpx
from app.config import settings


async def send_fcm_push(push_token: str, title: str, body: str, data: dict = None) -> bool:
    """
    Send push notification via Firebase Cloud Messaging
    """
    if not settings.fcm_server_key:
        print("⚠️ FCM_SERVER_KEY not configured, simulating push send")
        await asyncio.sleep(0.5)
        return True
    
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"Bearer {settings.fcm_server_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": push_token,
            "notification": {
                "title": title,
                "body": body
            },
            "data": data or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            if response.status_code == 200:
                print(f"✅ FCM push sent successfully")
                return True
            else:
                print(f"❌ FCM push failed: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Failed to send FCM push: {e}")
        raise e


async def send_onesignal_push(push_token: str, title: str, body: str, data: dict = None) -> bool:
    """
    Send push notification via OneSignal
    """
    if not settings.onesignal_app_id or not settings.onesignal_api_key:
        print("⚠️ OneSignal not configured, simulating push send")
        await asyncio.sleep(0.5)
        return True
    
    try:
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Authorization": f"Basic {settings.onesignal_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "app_id": settings.onesignal_app_id,
            "include_player_ids": [push_token],
            "headings": {"en": title},
            "contents": {"en": body},
            "data": data or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            if response.status_code == 200:
                print(f"✅ OneSignal push sent successfully")
                return True
            else:
                print(f"❌ OneSignal push failed: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Failed to send OneSignal push: {e}")
        raise e


async def send_push_notification(push_token: str, title: str, body: str, data: dict = None) -> bool:
    """
    Send push notification (auto-select provider)
    """
    # Try FCM first if configured
    if settings.fcm_server_key:
        return await send_fcm_push(push_token, title, body, data)
    
    # Try OneSignal if configured
    if settings.onesignal_app_id and settings.onesignal_api_key:
        return await send_onesignal_push(push_token, title, body, data)
    
    # Simulate if no provider configured (for testing)
    print(f"📱 Simulating push to {push_token}: {title} - {body}")
    await asyncio.sleep(0.5)
    return True
