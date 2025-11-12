from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service
    user_service_port: int = 8001
    
    # Database (PostgreSQL connection string)
    database_url: str = "postgresql+asyncpg://notification_user:notification_password@postgres:5432/user_service_db"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    
    # JWT Authentication
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    
    # Logging
    log_level: str = "info"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
