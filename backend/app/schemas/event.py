from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# Shared properties
class EventBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    capacity: Optional[int] = None

class EventCreate(EventBase):
    title: str
    start_time: datetime
    end_time: datetime
    location: str
    capacity: Optional[int] = None

class EventUpdate(EventBase):
    pass

class EventInDBBase(EventBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass

class EventInDB(EventInDBBase):
    pass

# Participant Schemas
class ParticipantStatus(str, Enum):
    GOING = "going"
    INTERESTED = "interested"
    NOT_GOING = "not_going"

class EventParticipantBase(BaseModel):
    status: ParticipantStatus = ParticipantStatus.INTERESTED

class EventParticipantCreate(EventParticipantBase):
    user_id: int
    event_id: int

class EventParticipantUpdate(EventParticipantBase):
    pass

class EventParticipant(EventParticipantBase):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
