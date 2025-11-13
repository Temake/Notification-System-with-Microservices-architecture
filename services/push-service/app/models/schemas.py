from typing import Dict, Optional
from pydantic import BaseModel
from enum import Enum


class NotificationStatus(str, Enum):
    sent = "sent"
    pending = "pending"
    failed = "failed"


class PushSendRequest(BaseModel):
    notification_id: str
    user_id: str
    template_code: str
    variables: Dict[str, str]
    priority: int = 1
    retry_count: int = 0


class PushNotification(BaseModel):
    user_id: str
    title: str
    message: str
    image_url: Optional[str] = None
    link: Optional[str] = None
    status: NotificationStatus
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class PushSendResponse(BaseModel):
    notification_id: str
    status: str
    message: str
