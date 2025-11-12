"""
RabbitMQ Consumer Worker
Listens to email.queue and processes email notifications
"""
import pika
import json
import asyncio
from datetime import datetime
from app.config import settings
from app.services.email_sender import send_email
from app.services.template_client import render_template
from app.services.user_client import get_user
from app.utils.retry import retry_with_backoff


@retry_with_backoff(max_attempts=settings.max_retry_attempts, delay=settings.retry_delay_seconds)
async def process_email(message_data: dict):
    """
    Process email notification
    """
    notification_id = message_data.get("notification_id")
    user_id = message_data.get("user_id")
    template_code = message_data.get("template_code")
    variables = message_data.get("variables", {})
    
    print(f"📧 Processing email notification: {notification_id}")
    
    # 1. Get user email from User Service
    user = await get_user(user_id)
    if not user or not user.get("email"):
        raise Exception(f"User {user_id} not found or no email")
    
    user_email = user["email"]
    
    # Check if user has email preference enabled
    preferences = user.get("preferences", {})
    if not preferences.get("email", True):
        print(f"⚠️ User {user_id} has disabled email notifications")
        return
    
    # 2. Render template
    rendered = await render_template(template_code, variables)
    if not rendered:
        raise Exception(f"Failed to render template: {template_code}")
    
    subject = rendered.get("subject", "Notification")
    body = rendered.get("body", "")
    
    # 3. Send email via Gmail
    await send_email(user_email, subject, body)
    
    print(f"✅ Email sent successfully to {user_email}")


def callback(ch, method, properties, body):
    """RabbitMQ message callback"""
    try:
        message_data = json.loads(body)
        print(f"📨 Received message: {message_data.get('notification_id')}")
        
        # Run async function
        asyncio.run(process_email(message_data))
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        # Reject and requeue with retry limit
        retry_count = message_data.get("retry_count", 0)
        if retry_count < settings.max_retry_attempts:
            message_data["retry_count"] = retry_count + 1
            ch.basic_publish(
                exchange='',
                routing_key=settings.email_queue_name,
                body=json.dumps(message_data)
            )
        else:
            # Send to dead letter queue
            ch.basic_publish(
                exchange='',
                routing_key='failed.queue',
                body=json.dumps(message_data)
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """Start RabbitMQ consumer"""
    print("🔌 Connecting to RabbitMQ...")
    
    credentials = pika.PlainCredentials(
        settings.rabbitmq_user,
        settings.rabbitmq_password
    )
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            virtual_host=settings.rabbitmq_vhost,
            credentials=credentials
        )
    )
    
    channel = connection.channel()
    channel.queue_declare(queue=settings.email_queue_name, durable=True)
    channel.queue_declare(queue='failed.queue', durable=True)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=settings.email_queue_name,
        on_message_callback=callback
    )
    
    print(f"✅ Listening to {settings.email_queue_name}...")
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
