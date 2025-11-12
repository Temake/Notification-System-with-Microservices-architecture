from typing import Dict
from pydantic import BaseModel, EmailStr


class EmailSendRequest(BaseModel):
    notification_id: str
    user_id: str
    template_code: str
    variables: Dict[str, str]
    priority: int = 1
    retry_count: int = 0


class EmailSendResponse(BaseModel):
    notification_id: str
    status: str
    message: str
