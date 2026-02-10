import logging
from typing import Dict, Any
from .base import BaseNotificationProvider

logger = logging.getLogger(__name__)

class MockNotificationProvider(BaseNotificationProvider):
    async def send_notification(self, user_id: int, title: str, body: str, data: Dict[str, Any] = None) -> bool:
        logger.info(f"PUSH NOTIFICATION [Mock] -> User {user_id}: {title} - {body} | Data: {data}")
        return True
