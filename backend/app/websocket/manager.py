import asyncio
import json
import logging
from typing import List, Dict
import redis.asyncio as redis
from fastapi import WebSocket

from app.core.config import settings

# Initialize logging
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Map event_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Redis connection - will be initialized on first use
        self.redis = None
        self.pubsub = None
        self._redis_initialized = False

    async def _ensure_redis(self):
        """Initialize Redis connection if not already done"""
        if not self._redis_initialized:
            self.redis = await redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.pubsub = self.redis.pubsub()
            self._redis_initialized = True

    async def connect(self, websocket: WebSocket, event_id: int):
        await self._ensure_redis()
        await websocket.accept()
        event_key = str(event_id)
        if event_key not in self.active_connections:
            self.active_connections[event_key] = []
            # Start subscribing to Redis channel for this event if first connection
            await self.subscribe_to_channel(event_key)
            
        self.active_connections[event_key].append(websocket)
        logger.info(f"WebSocket connected to event {event_id}. Total connections: {len(self.active_connections[event_key])}")

    def disconnect(self, websocket: WebSocket, event_id: int):
        event_key = str(event_id)
        if event_key in self.active_connections:
            if websocket in self.active_connections[event_key]:
                self.active_connections[event_key].remove(websocket)
            
            if not self.active_connections[event_key]:
                del self.active_connections[event_key]
                # In a real app, we might unsubscribe from Redis here if no one is listening locally
        logger.info(f"WebSocket disconnected from event {event_id}")

    async def broadcast_to_local(self, event_id: int, message: str):
        """
        Send a message to all locally connected clients for this event.
        """
        event_key = str(event_id)
        if event_key in self.active_connections:
            for connection in self.active_connections[event_key]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message to client: {e}")

    async def publish_message(self, event_id: int, message: dict):
        """
        Publish message to Redis so other instances can pick it up.
        """
        await self._ensure_redis()
        channel = f"chat:{event_id}"
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe_to_channel(self, event_id: str):
        """
        Subscribe to Redis channel and listen for messages in background.
        """
        await self._ensure_redis()
        channel = f"chat:{event_id}"
        await self.pubsub.subscribe(channel)
        
        # We need a background task to listen to this channel
        asyncio.create_task(self.redis_listener(channel, event_id))

    async def redis_listener(self, channel: str, event_id: str):
        """
        Listen to Redis channel and broadcast to local clients.
        """
        await self._ensure_redis()
        logger.info(f"Started Redis listener for {channel}")
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    content = message["data"]
                    # Broadcast to local websocket connections
                    await self.broadcast_to_local(int(event_id), content)
        except Exception as e:
            logger.error(f"Error in Redis listener for {channel}: {e}")

manager = ConnectionManager()
