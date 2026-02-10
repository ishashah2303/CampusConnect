from typing import List, Optional
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class ParticipantStatus(str, enum.Enum):
    GOING = "going"
    INTERESTED = "interested"
    NOT_GOING = "not_going"

class Event(Base):
    # Base class columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Event-specific columns
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # None means unlimited
    
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="events_created")
    participants: Mapped[List["EventParticipant"]] = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="event", cascade="all, delete-orphan")

class EventParticipant(Base):
    # Base class columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # EventParticipant-specific columns
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("event.id"), nullable=False)
    status: Mapped[ParticipantStatus] = mapped_column(SQLEnum(ParticipantStatus), default=ParticipantStatus.INTERESTED, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="event_participations")
    event: Mapped["Event"] = relationship("Event", back_populates="participants")
