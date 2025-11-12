
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class NotificationStatusEnum(str, Enum):
    """Notification status"""
    pending = "pending"
    delivered = "delivered"
    failed = "failed"


class NotificationLog(SQLModel, table=True):

    __tablename__ = "notification_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    request_id: str = Field(index=True, unique=True)  # For idempotency
    user_id: str = Field(index=True)
    notification_type: str  # "email" or "push"
    template_code: str
    status: str = Field(default="pending")  # pending, delivered, failed
    priority: int = Field(default=1)
    error_message: Optional[str] = None
    retry_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None


# Example: You can add more models as needed
# class RateLimitLog(SQLModel, table=True):
#     """Track rate limits per user"""
#     __tablename__ = "rate_limit_logs"
#     
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: str = Field(index=True)
#     request_count: int = Field(default=0)
#     window_start: datetime = Field(default_factory=datetime.utcnow)
