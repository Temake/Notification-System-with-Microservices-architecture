from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserPreference(BaseModel):
    email: bool = True
    push: bool = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    push_token: Optional[str] = None
    preferences: Optional[UserPreference] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    push_token: Optional[str] = None


class UserPreferenceUpdate(BaseModel):
    email: Optional[bool] = None
    push: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    push_token: Optional[str] = None
    preferences: UserPreference
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
