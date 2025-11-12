# Distributed Notification System

A microservices-based notification system that sends emails and push notifications using message queues for asynchronous communication.

## Architecture Overview

This system consists of 5 microservices:
- **API Gateway**: Entry point for all notification requests
- **User Service**: Manages user data and preferences
- **Email Service**: Processes email notifications
- **Push Service**: Handles push notifications
- **Template Service**: Manages notification templates

## Tech Stack

- **Language**: Node.js (TypeScript)
- **Message Queue**: RabbitMQ
- **Database**: PostgreSQL
- **Cache**: Redis
- **Containerization**: Docker

## Services

### API Gateway (Port: 3000)
- Validates and authenticates requests
- Routes messages to correct queues
- Tracks notification status
- Health checks at `/health`

### User Service (Port: 3001)
- User management and authentication
- Contact info (email, push tokens)
- Notification preferences
- Health checks at `/health`

### Email Service (Port: 3002)
- Consumes from `email.queue`
- Template rendering
- SMTP/API delivery (SendGrid, Mailgun)
- Delivery tracking

### Push Service (Port: 3003)
- Consumes from `push.queue`
- FCM/OneSignal integration
- Device token validation
- Rich notifications support

### Template Service (Port: 3004)
- Template CRUD operations
- Variable substitution
- Multi-language support
- Version history

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)

### Setup

1. Clone the repository
```bash
git clone <repository-url>
cd stage4
```

2. Copy environment files
```bash
cp .env.example .env
```

3. Start all services
```bash
docker-compose up -d
```

4. Check service health
```bash
curl http://localhost:3000/health
```

## Development

### Run individual service locally
```bash
cd services/api-gateway
npm install
npm run dev
```

### Run tests
```bash
npm test
```

## Message Queue Structure

```
Exchange: notifications.direct
├── email.queue    → Email Service
├── push.queue     → Push Service
└── failed.queue   → Dead Letter Queue
```

## API Documentation

Swagger documentation available at:
- API Gateway: http://localhost:3000/api-docs

## Key Features

- ✅ Circuit Breaker pattern
- ✅ Exponential backoff retry
- ✅ Idempotency with request IDs
- ✅ Service discovery
- ✅ Health monitoring
- ✅ Distributed logging

## Performance Targets

- Handle 1,000+ notifications/minute
- API Gateway response < 100ms
- 99.5% delivery success rate
- Horizontal scaling support

## Team

[Add team member names here]

## License

MIT
