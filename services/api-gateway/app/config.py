"""
Configuration settings for API Gateway
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_gateway_port: int = 8000
    jwt_secret: str = "change-me-in-production"
    api_rate_limit: int = 100
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_vhost: str = "/"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    user_service_url: str = "http://localhost:8001"
    template_service_url: str = "http://localhost:8004"
    log_level: str = "info"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
