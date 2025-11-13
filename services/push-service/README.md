# Push Service

## Overview
Processes push notifications from RabbitMQ queue and sends them via Firebase Cloud Messaging (FCM) or OneSignal.

## Stack
- **Framework**: FastAPI (Python 3.10+)
- **Push Provider**: FCM / OneSignal
- **Message Queue**: RabbitMQ (Consumer)
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLModel

## Features
- Consumes messages from `push.queue`
- Sends push notifications via FCM/OneSignal
- Fetches templates from Template Service
- Fetches user data from User Service
- Retry logic with exponential backoff
- Dead letter queue for failed messages
- Supports rich notifications (title, body, image, link)

## Setup

### Push Provider Configuration

#### Option 1: Firebase Cloud Messaging (FCM)
1. Go to Firebase Console: https://console.firebase.google.com/
2. Create/Select project
3. Go to Project Settings → Service Accounts
4. Generate new private key (JSON file)
5. Save as `fcm-credentials.json` or set `FCM_SERVER_KEY`

#### Option 2: OneSignal (Recommended for simplicity)
1. Sign up at https://onesignal.com/
2. Create new app
3. Get App ID and REST API Key
4. Add to `.env`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
```bash
cp .env.example .env
# Edit .env with your push provider credentials
```

### Run Service
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003

# Production (with background worker)
python -m app.worker &
uvicorn app.main:app --host 0.0.0.0 --port 8003 --workers 4
```

## Message Format

Expected message from RabbitMQ `push.queue`:
```json
{
  "notification_id": "uuid",
  "user_id": "uuid",
  "template_code": "welcome_push",
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

## Project Structure
```
push-service/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── worker.py            # RabbitMQ consumer
│   ├── models/
│   │   ├── db_models.py     # Push log table
│   │   └── schemas.py       # Request/response models
│   ├── services/
│   │   ├── push_sender.py   # FCM/OneSignal logic
│   │   ├── template_client.py
│   │   └── user_client.py
│   └── utils/
│       └── retry.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Environment Variables
See `.env.example` for all configuration options.
