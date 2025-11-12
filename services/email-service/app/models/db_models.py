from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class EmailLog(SQLModel, table=True):
    __tablename__ = "email_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    email_to: str
    subject: str
    template_code: str
    status: str = Field(default="pending")  # pending, sent, failed
    retry_count: int = Field(default=0)
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
