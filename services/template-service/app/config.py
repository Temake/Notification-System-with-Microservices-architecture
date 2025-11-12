from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    template_service_port: int = 8004
    database_url: str = "postgresql+asyncpg://notification_user:notification_password@postgres:5432/template_service_db"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    log_level: str = "info"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
