import asyncio


async def send_push_notification(push_data: dict):
    print(
        f"Sending push notification to user {push_data['user_id']} with title '{push_data['title']}'"
    )
    await asyncio.sleep(1)  # Simulate network delay
    return {"status": "success", "detail": "Notification sent"}
