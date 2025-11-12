import asyncio
import json

import aio_pika


async def publish_test():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    channel = await connection.channel()

    message = {
        "user_id": "12345",
        "title": "Test Notification",
        "message": "This is a test push notification.",
        "request_id": "req-67890",
        "status": "pending",
    }

    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key="push.queue",
    )
    print(f"Sent message: {message}")


if __name__ == "__main__":
    asyncio.run(publish_test())
