from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service
    email_service_port: int = 8002
    
    # Database (PostgreSQL connection string)
    database_url: str = "postgresql+asyncpg://notification_user:notification_password@postgres:5432/email_service_db"
    
    # Gmail SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "Notification System"
    
    # RabbitMQ
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_vhost: str = "/"
    email_queue_name: str = "email.queue"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    
    # Service URLs
    user_service_url: str = "http://localhost:8001"
    template_service_url: str = "http://localhost:8004"
    api_gateway_url: str = "http://localhost:8000"
    
    # Retry Configuration
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 5
    
    # Logging
    log_level: str = "info"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
