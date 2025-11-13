from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Push Service...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized!")
    yield
    print("👋 Shutting down Push Service...")


app = FastAPI(
    title="Push Service",
    description="Processes push notifications",
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
        "message": "Push Service is healthy",
        "data": {"service": "push-service", "status": "running"}
    }


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Push Service API",
        "data": {"version": "1.0.0", "docs": "/docs"}
    }
