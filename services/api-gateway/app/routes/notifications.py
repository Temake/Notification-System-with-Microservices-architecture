"""
Notification routes with database integration
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import uuid
from datetime import datetime

from app.models import NotificationRequest, ApiResponse
from app.models.db_models import NotificationLog
from app.database import get_session

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=ApiResponse)
async def send_notification(
    notification: NotificationRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Send a notification request
    
    Steps:
    1. Check idempotency (request_id) - prevents duplicate sends
    2. Create notification log in database
    3. TODO: Validate user_id (call User Service)
    4. TODO: Validate template_code (call Template Service)
    5. TODO: Route to appropriate queue (email/push)
    """
    # Check if request_id already exists (idempotency)
    result = await session.execute(
        select(NotificationLog).where(NotificationLog.request_id == notification.request_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return {
            "success": True,
            "message": "Notification already processed (idempotent)",
            "data": {
                "notification_id": existing.notification_id,
                "status": existing.status
            }
        }
    
    # Create new notification log
    notification_id = str(uuid.uuid4())
    log = NotificationLog(
        notification_id=notification_id,
        request_id=notification.request_id,
        user_id=notification.user_id,
        notification_type=notification.notification_type.value,
        template_code=notification.template_code,
        status="pending",
        priority=notification.priority,
    )
    
    session.add(log)
    await session.commit()
    await session.refresh(log)
    
    # TODO: Publish to RabbitMQ queue
    # TODO: Call User Service to validate user
    # TODO: Call Template Service to get template
    
    return {
        "success": True,
        "message": "Notification queued successfully",
        "data": {
            "notification_id": notification_id,
            "status": "pending"
        }
    }


@router.get("/{notification_id}/status", response_model=ApiResponse)
async def get_notification_status(
    notification_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Get notification status from database
    """
    result = await session.execute(
        select(NotificationLog).where(NotificationLog.notification_id == notification_id)
    )
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {
        "success": True,
        "message": "Status retrieved",
        "data": {
            "notification_id": log.notification_id,
            "status": log.status,
            "notification_type": log.notification_type,
            "created_at": log.created_at.isoformat(),
            "updated_at": log.updated_at.isoformat(),
            "delivered_at": log.delivered_at.isoformat() if log.delivered_at else None,
            "error_message": log.error_message,
            "retry_count": log.retry_count
        }
    }
