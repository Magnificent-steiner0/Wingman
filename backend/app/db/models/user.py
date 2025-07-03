from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), # native UUID in postgres; mapped to uuid.UUID in Python
        primary_key=True,
        default=uuid.uuid4 # uuid4 is completely random and good for primary key
        )
    
    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
        )
    
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False
    )
    
    # if the user is verified their email or not. default is False
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False 
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    
    # if the user is signed in by google
    is_oauth_user: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default = datetime.now(timezone.utc)
    )