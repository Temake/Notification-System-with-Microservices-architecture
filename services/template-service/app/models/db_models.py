from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, JSON, Column
from enum import Enum


class NotificationType(str, Enum):
    email = "email"
    push = "push"


class Template(SQLModel, table=True):
    __tablename__ = "templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    template_code: str = Field(index=True, unique=True)
    name: str
    notification_type: str
    subject: Optional[str] = None  # For email templates
    body: str
    language: str = Field(default="en", index=True)
    variables: List[str] = Field(default=[], sa_column=Column(JSON))
    version: int = Field(default=1)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
