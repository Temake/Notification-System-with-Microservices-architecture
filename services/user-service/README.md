# User Service

## Overview
Manages user data, authentication, and notification preferences.

## Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLModel
- **Auth**: JWT

## Features
- User CRUD operations
- User authentication (login/register)
- Notification preferences management
- Password hashing with bcrypt
- JWT token generation
- Redis caching for user data

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

## API Endpoints

### Health Check
```
GET /health
```

### User Management

#### Register User
```
POST /api/v1/users/
```
Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "push_token": "fcm-token-here",
  "preferences": {
    "email": true,
    "push": true
  }
}
```

#### Login
```
POST /api/v1/users/login
```
Request:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

#### Get User
```
GET /api/v1/users/{user_id}
```

#### Update User
```
PUT /api/v1/users/{user_id}
```

#### Update Preferences
```
PUT /api/v1/users/{user_id}/preferences
```
Request:
```json
{
  "email": true,
  "push": false
}
```

## Project Structure
```
user-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── db_models.py     # User table
│   │   ├── schemas.py       # Request/response models
│   │   └── response.py      # Standard response
│   ├── routes/
│   │   └── users.py
│   └── utils/
│       ├── auth.py          # JWT & password hashing
│       └── cache.py         # Redis caching
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Environment Variables
See `.env.example` for all configuration options.
