from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class PushLog(SQLModel, table=True):
    __tablename__ = "push_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    push_token: str
    title: str
    message: str
    template_code: str
    status: str = Field(default="pending")  # pending, sent, failed
    retry_count: int = Field(default=0)
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
