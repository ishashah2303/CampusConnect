from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseNotificationProvider(ABC):
    @abstractmethod
    async def send_notification(self, user_id: int, title: str, body: str, data: Dict[str, Any] = None) -> bool:
        """
        Send a notification to a specific user.
        """
        pass
