from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional, List
from datetime import datetime

from app.database import get_session
from app.models.db_models import Template
from app.models import (
    TemplateCreate,
    TemplateResponse,
    TemplateRenderRequest,
    TemplateRenderResponse,
    ApiResponse
)
from app.utils.template_engine import render_template
from app.utils.cache import cache_template, get_cached_template, invalidate_cache

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("/", response_model=ApiResponse[TemplateResponse])
async def create_template(
    template: TemplateCreate,
    session: AsyncSession = Depends(get_session)
):
    # Check if template_code already exists
    result = await session.execute(
        select(Template).where(Template.template_code == template.template_code)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Template code already exists")
    
    # Create template
    db_template = Template(**template.model_dump())
    session.add(db_template)
    await session.commit()
    await session.refresh(db_template)
    
    return {
        "success": True,
        "message": "Template created successfully",
        "data": db_template
    }


@router.get("/{template_code}", response_model=ApiResponse[TemplateResponse])
async def get_template(
    template_code: str,
    session: AsyncSession = Depends(get_session)
):
    # Try cache first
    cached = await get_cached_template(template_code)
    if cached:
        return {
            "success": True,
            "message": "Template retrieved from cache",
            "data": cached
        }
    
    # Query database
    result = await session.execute(
        select(Template).where(
            Template.template_code == template_code,
            Template.is_active == True
        )
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Cache for future requests
    template_dict = template.model_dump()
    await cache_template(template_code, template_dict)
    
    return {
        "success": True,
        "message": "Template retrieved",
        "data": template
    }


@router.get("/", response_model=ApiResponse[List[TemplateResponse]])
async def list_templates(
    notification_type: Optional[str] = Query(None),
    language: Optional[str] = Query("en"),
    session: AsyncSession = Depends(get_session)
):
    query = select(Template).where(Template.is_active == True)
    
    if notification_type:
        query = query.where(Template.notification_type == notification_type)
    if language:
        query = query.where(Template.language == language)
    
    result = await session.execute(query)
    templates = result.scalars().all()
    
    return {
        "success": True,
        "message": f"Found {len(templates)} templates",
        "data": templates
    }


@router.post("/{template_code}/render", response_model=ApiResponse[TemplateRenderResponse])
async def render_template_endpoint(
    template_code: str,
    render_request: TemplateRenderRequest,
    session: AsyncSession = Depends(get_session)
):
    # Get template
    result = await session.execute(
        select(Template).where(
            Template.template_code == template_code,
            Template.is_active == True
        )
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Render template
    rendered_body = render_template(template.body, render_request.variables)
    rendered_subject = None
    if template.subject:
        rendered_subject = render_template(template.subject, render_request.variables)
    
    return {
        "success": True,
        "message": "Template rendered successfully",
        "data": {
            "subject": rendered_subject,
            "body": rendered_body
        }
    }


@router.delete("/{template_code}", response_model=ApiResponse)
async def delete_template(
    template_code: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Template).where(Template.template_code == template_code)
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Soft delete
    template.is_active = False
    template.updated_at = datetime.utcnow()
    await session.commit()
    
    # Invalidate cache
    await invalidate_cache(template_code)
    
    return {
        "success": True,
        "message": "Template deleted successfully",
        "data": None
    }
