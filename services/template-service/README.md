# Template Service

## Overview
Manages notification templates with variable substitution, versioning, and multi-language support.

## Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLModel

## Features
- CRUD operations for templates
- Variable substitution (e.g., `{{name}}`, `{{link}}`)
- Template versioning
- Multi-language support
- Redis caching for performance

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### Run Service
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8004

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8004 --workers 4
```

## API Endpoints

### Health Check
```
GET /health
```

### Templates

#### Create Template
```
POST /api/v1/templates/
```
Request:
```json
{
  "template_code": "welcome_email",
  "name": "Welcome Email",
  "notification_type": "email",
  "subject": "Welcome to {{app_name}}!",
  "body": "Hi {{name}}, welcome to our platform!",
  "language": "en",
  "variables": ["name", "app_name"]
}
```

#### Get Template
```
GET /api/v1/templates/{template_code}
```

#### List Templates
```
GET /api/v1/templates/?notification_type=email&language=en
```

#### Render Template
```
POST /api/v1/templates/{template_code}/render
```
Request:
```json
{
  "variables": {
    "name": "John Doe",
    "app_name": "MyApp"
  }
}
```

Response:
```json
{
  "success": true,
  "message": "Template rendered",
  "data": {
    "subject": "Welcome to MyApp!",
    "body": "Hi John Doe, welcome to our platform!"
  }
}
```

## Project Structure
```
template-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── db_models.py
│   │   ├── schemas.py
│   │   └── response.py
│   ├── routes/
│   │   └── templates.py
│   └── utils/
│       ├── cache.py
│       └── template_engine.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Environment Variables
See `.env.example` for all configuration options.
