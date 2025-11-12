# API Gateway Service

## Overview
Entry point for all notification requests. Validates, authenticates, and routes messages to the appropriate queue.

## Stack
- **Framework**: FastAPI (Python 3.10+)
- **Message Queue**: RabbitMQ
- **Cache**: Redis
- **Authentication**: JWT

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip or poetry

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Run the service:
```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
```
GET /health
```

### Notifications
```
POST /api/v1/notifications/
```

Request Body:
```json
{
  "notification_type": "email",
  "user_id": "uuid",
  "template_code": "welcome_email",
  "variables": {
    "name": "John Doe",
    "link": "https://example.com"
  },
  "request_id": "unique-request-id",
  "priority": 1,
  "metadata": {}
}
```

### Notification Status
```
GET /api/v1/notifications/{notification_id}/status
```

## Key Features

### 1. Request Validation
- Schema validation using Pydantic
- Authentication & authorization
- Idempotency checks

### 2. Queue Routing
- Routes to `email.queue` or `push.queue`
- Priority handling
- Dead letter queue for failures

### 3. Circuit Breaker
- Prevents cascading failures
- Automatic recovery
- Fallback mechanisms

### 4. Rate Limiting
- Per-user rate limits using Redis
- Global rate limits
- Configurable thresholds

## Project Structure

```
api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── notification.py  # Notification models
│   │   └── response.py      # Response models
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── notifications.py # Notification routes
│   │   └── health.py        # Health check routes
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── queue_service.py # Message queue operations
│   │   └── auth_service.py  # Authentication
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth middleware
│   │   └── rate_limit.py    # Rate limiting
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── circuit_breaker.py
│       └── logger.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Docker Deployment

Build image:
```bash
docker build -t api-gateway .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env api-gateway
```

## Testing

Run tests:
```bash
pytest tests/
```

## Monitoring

- Logs: Structured JSON logs with correlation IDs
- Metrics: Request count, latency, error rates
- Health: `/health` endpoint for liveness probes

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `RABBITMQ_HOST`, `RABBITMQ_PORT`
- `REDIS_HOST`, `REDIS_PORT`
- `JWT_SECRET`
- `API_RATE_LIMIT`
