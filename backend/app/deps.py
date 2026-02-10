from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app import models, schemas
from app.db import session

# Placeholder for DB session (Mocking for now as we don't have DB connection code fully wired up)
# In a real app, this would use SessionLocal from db/session.py
def get_db() -> Generator:
    try:
        db = session.SessionLocal()
        yield db
    finally:
        db.close()
    # pass # For now, just pass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(sub=user_id)
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == token_data.sub).first()
    if not user:
        raise credentials_exception
    return user
