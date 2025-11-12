"""
API Gateway - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Notification API Gateway",
    description="Entry point for distributed notification system",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "API Gateway is healthy",
        "data": {
            "service": "api-gateway",
            "status": "running"
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "success": True,
        "message": "Notification API Gateway",
        "data": {
            "version": "1.0.0",
            "docs": "/docs"
        }
    }

# TODO: Import and include routers
# from app.routes import notifications, health
# app.include_router(notifications.router, prefix="/api/v1")
# app.include_router(health.router)
