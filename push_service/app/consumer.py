import asyncio

import aio_pika
from models import PushNotification
from push_sender import send_push_notification

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "push.queue"


async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            push_data = PushNotification.model_validate_json(message.body.decode())
            result = await send_push_notification(push_data.dict())
            print(f"Push notification result: {result}")
        except Exception as e:
            print(f"Failed to process message: {e}")


async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(callback)
    print("Push notification consumer started. Waiting for messages...")
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
