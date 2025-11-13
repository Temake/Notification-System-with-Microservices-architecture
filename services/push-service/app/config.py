from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service
    push_service_port: int = 8003
    
    # Database (PostgreSQL connection string)
    database_url: str = "postgresql+asyncpg://notification_user:notification_password@postgres:5432/push_service_db"
    
    # Push Providers
    fcm_server_key: str = ""
    onesignal_app_id: str = ""
    onesignal_api_key: str = ""
    
    # RabbitMQ
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_vhost: str = "/"
    push_queue_name: str = "push.queue"
    
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
