from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "authly"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True, default="")
    last_name = Column(String(100), nullable=True, default="")
    email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Use a callable to import the RefreshToken model only when needed
    refresh_tokens = relationship(
        lambda: __import__('app.models.refresh_token', fromlist=['RefreshToken']).RefreshToken,
        back_populates="user",
        cascade="all, delete-orphan"
    )
