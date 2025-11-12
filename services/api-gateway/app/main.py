from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Create database tables
    print("🚀 Starting API Gateway...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down API Gateway...")


app = FastAPI(
    title="Notification API Gateway",
    description="Entry point for distributed notification system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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


# Include routers
from app.routes import notifications
app.include_router(notifications.router, prefix="/api/v1")
