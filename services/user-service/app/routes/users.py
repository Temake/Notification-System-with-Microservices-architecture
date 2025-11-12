from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime

from app.database import get_session
from app.models.db_models import User, UserPreferences
from app.models.schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserPreferenceUpdate,
    UserResponse,
    LoginResponse,
    UserPreference
)
from app.models.response import ApiResponse
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.cache import cache_user, get_cached_user, invalidate_user_cache

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ApiResponse[UserResponse])
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user"""
    # Check if email exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    preferences = UserPreferences(**(user_data.preferences.model_dump() if user_data.preferences else {}))
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        push_token=user_data.push_token,
        preferences=preferences
    )
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return {
        "success": True,
        "message": "User created successfully",
        "data": user
    }


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    """User login"""
    result = await session.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    # Create JWT token
    token = create_access_token({"sub": str(user.id), "email": user.email})
    
    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }
    }


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get user by ID"""
    # Try cache first
    cached = await get_cached_user(user_id)
    if cached:
        return {
            "success": True,
            "message": "User retrieved from cache",
            "data": cached
        }
    
    # Query database
    result = await session.execute(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cache for future requests
    user_dict = user.model_dump()
    await cache_user(user_id, user_dict)
    
    return {
        "success": True,
        "message": "User retrieved",
        "data": user
    }


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update user"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if user_data.name:
        user.name = user_data.name
    if user_data.push_token is not None:
        user.push_token = user_data.push_token
    
    user.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(user)
    
    # Invalidate cache
    await invalidate_user_cache(user_id)
    
    return {
        "success": True,
        "message": "User updated successfully",
        "data": user
    }


@router.put("/{user_id}/preferences", response_model=ApiResponse[UserResponse])
async def update_preferences(
    user_id: int,
    preferences: UserPreferenceUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update user notification preferences"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update preferences
    current_prefs = user.preferences
    if preferences.email is not None:
        current_prefs.email = preferences.email
    if preferences.push is not None:
        current_prefs.push = preferences.push
    
    user.preferences = current_prefs
    user.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(user)
    
    # Invalidate cache
    await invalidate_user_cache(user_id)
    
    return {
        "success": True,
        "message": "Preferences updated successfully",
        "data": user
    }


@router.delete("/{user_id}", response_model=ApiResponse)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete user (soft delete)"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    user.updated_at = datetime.utcnow()
    await session.commit()
    
    # Invalidate cache
    await invalidate_user_cache(user_id)
    
    return {
        "success": True,
        "message": "User deleted successfully",
        "data": None
    }
