from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

# Initialize Argon2 password hasher
# Argon2 is more secure than bcrypt and doesn't have the 72-byte password limit
password_hasher = PasswordHasher()

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against an Argon2 hash.
    Returns True if password matches, False otherwise.
    """
    try:
        password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception:
        # Handle any other exceptions (e.g., invalid hash format)
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2.
    Argon2 supports passwords of any length (unlike bcrypt's 72-byte limit).
    """
    return password_hasher.hash(password)
