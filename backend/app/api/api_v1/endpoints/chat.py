from typing import Any
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app import models, schemas
from app import deps
from app.core import config
from app.websocket.manager import manager
from app.services import chat as chat_service
from app.services.notification.service import notification_service
from app.db.session import SessionLocal

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=10)

def get_db_sync():
    """Create a synchronous database session for use in async context"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Will be closed manually

@router.websocket("/ws/chat/{event_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    event_id: int,
    token: str = Query(...),
):
    # Authenticate via token
    user_id_int = None
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            await websocket.close(code=4003) # Forbidden
            return
        user_id_int = int(user_id)
        
        # Verify user exists
        db = get_db_sync()
        try:
            user = db.query(models.User).filter(models.User.id == user_id_int).first()
            if not user:
                await websocket.close(code=4003)
                return
        finally:
            db.close()
    except (JWTError, ValueError):
        await websocket.close(code=4003)
        return

    await manager.connect(websocket, event_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Save message to DB using thread pool for sync DB operations
            loop = asyncio.get_event_loop()
            db = get_db_sync()
            try:
                saved_msg = await loop.run_in_executor(
                    executor, 
                    chat_service.save_message, 
                    db, user_id_int, event_id, data
                )
                
                message_data = {
                    "id": saved_msg.id,
                    "content": saved_msg.content,
                    "sender_id": saved_msg.sender_id,
                    "event_id": saved_msg.event_id,
                    "created_at": str(saved_msg.created_at)
                }
                
                # Publish to Redis -> Broadcast to all
                await manager.publish_message(event_id, message_data)
            finally:
                db.close()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, event_id)
    except Exception as e:
        # Handle other errors
        manager.disconnect(websocket, event_id)
