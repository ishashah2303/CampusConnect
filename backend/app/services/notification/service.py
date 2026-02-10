import asyncio
from typing import Dict, Any, List
from .base import BaseNotificationProvider
from .mock_provider import MockNotificationProvider

# Facade service to handle notifications
class NotificationService:
    def __init__(self):
        self.provider: BaseNotificationProvider = MockNotificationProvider()

    async def send_to_user(self, user_id: int, title: str, body: str, data: Dict[str, Any] = None):
        # In a real app, this would push to a queue (Celery/BullMQ)
        # For this demo, we run it as an asyncio task
        asyncio.create_task(self.provider.send_notification(user_id, title, body, data))

    async def send_event_joined(self, user_id: int, event_title: str):
        await self.send_to_user(
            user_id,
            "Event Joined",
            f"You have successfully joined {event_title}.",
            {"type": "event_joined"}
        )

    async def send_new_message(self, user_id: int, sender_name: str, event_title: str, message_preview: str):
        # Logic to not notify if user is active in chat would go here
        await self.send_to_user(
            user_id,
            f"New message in {event_title}",
            f"{sender_name}: {message_preview}",
            {"type": "chat_message"}
        )

notification_service = NotificationService()
