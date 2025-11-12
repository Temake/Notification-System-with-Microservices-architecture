from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime


class TemplateCreate(BaseModel):
    template_code: str
    name: str
    notification_type: str  # "email" or "push"
    subject: Optional[str] = None
    body: str
    language: str = "en"
    variables: List[str] = []


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None


class TemplateResponse(BaseModel):
    id: int
    template_code: str
    name: str
    notification_type: str
    subject: Optional[str] = None
    body: str
    language: str
    variables: List[str]
    version: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TemplateRenderRequest(BaseModel):
    variables: Dict[str, str]


class TemplateRenderResponse(BaseModel):
    subject: Optional[str] = None
    body: str
