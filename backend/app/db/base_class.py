from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import Integer, DateTime


class Base(DeclarativeBase):
    """Base class for all database models."""
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Define common columns that will be inherited
    # Note: These are defined here but each model will inherit them properly
    __abstract__ = False
