# Email Service

## Overview
Processes email notifications from RabbitMQ queue and sends them via Gmail SMTP.

## Stack
- **Framework**: FastAPI (Python 3.10+)
- **Email**: Gmail SMTP
- **Message Queue**: RabbitMQ (Consumer)
- **Cache**: Redis
- **ORM**: SQLModel

## Features
- Consumes messages from `email.queue`
- Sends emails via Gmail SMTP
- Fetches templates from Template Service
- Fetches user data from User Service
- Retry logic with exponential backoff
- Dead letter queue for failed messages
- Circuit breaker for external services

## Setup

### Gmail App Password
1. Enable 2FA on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this password in `.env` (not your regular password)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
```bash
cp .env.example .env
# Edit .env with your Gmail credentials
```

### Run Service
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002

# Production (with background worker)
python -m app.worker &
uvicorn app.main:app --host 0.0.0.0 --port 8002 --workers 4
```

## Message Format

Expected message from RabbitMQ `email.queue`:
```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "template_code": "welcome_email",
  "variables": {
    "name": "John Doe",
    "link": "https://example.com"
  },
  "priority": 1,
  "retry_count": 0
}
```

## API Endpoints

### Health Check
```
GET /health
```

### Manual Send (for testing)
```
POST /api/v1/email/send
```

## Project Structure
```
email-service/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── worker.py            # RabbitMQ consumer
│   ├── models/
│   │   ├── db_models.py     # Email log table
│   │   └── schemas.py       # Request/response models
│   ├── services/
│   │   ├── email_sender.py  # Gmail SMTP logic
│   │   ├── template_client.py  # Template Service client
│   │   └── user_client.py   # User Service client
│   └── utils/
│       ├── circuit_breaker.py
│       └── retry.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Environment Variables
See `.env.example` for all configuration options.
