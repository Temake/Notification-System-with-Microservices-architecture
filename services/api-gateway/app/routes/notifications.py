"""
Notification routes - TODO: Implement
"""
from fastapi import APIRouter, HTTPException
from app.models import NotificationRequest, ApiResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=ApiResponse)
async def send_notification(notification: NotificationRequest):
    """
    Send a notification request
    
    TODO: Implement:
    1. Validate user_id (call User Service)
    2. Check idempotency (request_id)
    3. Validate template_code (call Template Service)
    4. Route to appropriate queue (email/push)
    5. Return notification_id
    """
    return {
        "success": True,
        "message": "Notification queued successfully",
        "data": {
            "notification_id": "temp-id",
            "status": "pending"
        }
    }


@router.get("/{notification_id}/status", response_model=ApiResponse)
async def get_notification_status(notification_id: str):
    """
    Get notification status
    
    TODO: Implement:
    1. Query status from cache/database
    2. Return current status
    """
    return {
        "success": True,
        "message": "Status retrieved",
        "data": {
            "notification_id": notification_id,
            "status": "pending"
        }
    }
