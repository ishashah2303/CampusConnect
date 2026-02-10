from sqlalchemy.orm import Session
from app import models, schemas

def save_message(db: Session, user_id: int, event_id: int, content: str) -> models.ChatMessage:
    message = models.ChatMessage(
        content=content,
        sender_id=user_id,
        event_id=event_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
