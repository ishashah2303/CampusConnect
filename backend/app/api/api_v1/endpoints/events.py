from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app import deps
from app.services.notification.service import notification_service

router = APIRouter()

@router.post("/", response_model=schemas.Event)
def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.EventCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new event.
    """
    try:
        # Validate that end_time is after start_time
        if event_in.end_time <= event_in.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )
        
        event = models.Event(
            title=event_in.title,
            description=event_in.description,
            start_time=event_in.start_time,
            end_time=event_in.end_time,
            location=event_in.location,
            capacity=event_in.capacity,
            creator_id=current_user.id,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )

@router.get("/", response_model=List[schemas.Event])
def read_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve events.
    """
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
) -> Any:
    """
    Get event by ID.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    event_in: schemas.EventUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an event.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an event.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(event)
    db.commit()
    return event

@router.post("/{event_id}/join", response_model=schemas.EventParticipant)
def join_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Join an event.
    """
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if already joined
    participant = db.query(models.EventParticipant).filter(
        models.EventParticipant.event_id == event_id,
        models.EventParticipant.user_id == current_user.id
    ).first()
    
    if participant:
        raise HTTPException(status_code=400, detail="Already joined this event")

    # Check capacity
    if event.capacity is not None:
        count = db.query(models.EventParticipant).filter(
            models.EventParticipant.event_id == event_id,
            models.EventParticipant.status.in_([models.ParticipantStatus.GOING, models.ParticipantStatus.INTERESTED])
        ).count()
        if count >= event.capacity:
             raise HTTPException(status_code=400, detail="Event is at full capacity")

    participant = models.EventParticipant(
        event_id=event_id,
        user_id=current_user.id,
        status=models.ParticipantStatus.GOING
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    
    # Send notification (async, but we're in sync context - run in background)
    # Note: In production, use a proper task queue like Celery
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(notification_service.send_event_joined(current_user.id, event.title))
        else:
            loop.run_until_complete(notification_service.send_event_joined(current_user.id, event.title))
    except Exception:
        pass # Don't fail request if notification fails check logs
        
    return participant

@router.post("/{event_id}/leave", response_model=schemas.EventParticipant)
def leave_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Leave an event.
    """
    participant = db.query(models.EventParticipant).filter(
        models.EventParticipant.event_id == event_id,
        models.EventParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Not participating in this event")

    db.delete(participant)
    db.commit()
    return participant
