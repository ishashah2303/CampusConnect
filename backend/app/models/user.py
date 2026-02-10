from typing import List, Optional
from datetime import datetime
from sqlalchemy import Boolean, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class User(Base):
    # Base class columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # User-specific columns
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    # Relationships
    events_created: Mapped[List["Event"]] = relationship("Event", back_populates="creator")
    event_participations: Mapped[List["EventParticipant"]] = relationship("EventParticipant", back_populates="user")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="sender")
