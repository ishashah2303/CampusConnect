from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class ChatMessage(Base):
    # Base class columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # ChatMessage-specific columns
    content: Mapped[str] = mapped_column(String, nullable=False)
    
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("event.id"), nullable=False)
    
    # Relationships
    sender: Mapped["User"] = relationship("User", back_populates="messages")
    event: Mapped["Event"] = relationship("Event", back_populates="messages")
