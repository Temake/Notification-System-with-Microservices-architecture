from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Email Service...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized!")
    yield
    print("👋 Shutting down Email Service...")


app = FastAPI(
    title="Email Service",
    description="Processes email notifications",
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
        "message": "Email Service is healthy",
        "data": {"service": "email-service", "status": "running"}
    }


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Email Service API",
        "data": {"version": "1.0.0", "docs": "/docs"}
    }
