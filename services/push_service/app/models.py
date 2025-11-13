from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, HttpUrl


class NotificationStatus(str, Enum):
    SENT = "sent"
    PENDING = "pending"
    FAILED = "failed"


class PushNotification(BaseModel):
    user_id: str
    title: str
    message: str
    image_uurl: Optional[HttpUrl] = None
    link: Optional[HttpUrl] = None
    status: NotificationStatus
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
