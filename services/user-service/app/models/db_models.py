from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, JSON, Column


class UserPreferences(SQLModel):
    email: bool = True
    push: bool = True


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    push_token: Optional[str] = None
    preferences: UserPreferences = Field(default_factory=UserPreferences, sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
