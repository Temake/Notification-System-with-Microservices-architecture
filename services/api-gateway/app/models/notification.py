"""
Notification models
"""
from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, HttpUrl


class NotificationType(str, Enum):
    """Notification type enumeration"""
    email = "email"
    push = "push"


class UserData(BaseModel):
    """User data for template variables"""
    name: str
    link: HttpUrl
    meta: Optional[Dict] = None


class NotificationRequest(BaseModel):
    """Notification request model"""
    notification_type: NotificationType
    user_id: str
    template_code: str
    variables: UserData
    request_id: str
    priority: int = 1
    metadata: Optional[Dict] = None


class NotificationStatus(str, Enum):
    """Notification status enumeration"""
    delivered = "delivered"
    pending = "pending"
    failed = "failed"


class NotificationStatusUpdate(BaseModel):
    """Notification status update model"""
    notification_id: str
    status: NotificationStatus
    timestamp: Optional[str] = None
    error: Optional[str] = None
