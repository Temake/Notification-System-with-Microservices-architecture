from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Template Service...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized!")
    yield
    print("👋 Shutting down Template Service...")


app = FastAPI(
    title="Template Service",
    description="Manages notification templates",
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
    return {
        "success": True,
        "message": "Template Service is healthy",
        "data": {"service": "template-service", "status": "running"}
    }


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Template Service API",
        "data": {"version": "1.0.0", "docs": "/docs"}
    }


# Include routers
from app.routes import templates
app.include_router(templates.router, prefix="/api/v1")
