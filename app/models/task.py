from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_dt = Column(DateTime(timezone=True), nullable=False)
    end_dt = Column(DateTime(timezone=True), nullable=True)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="tasks")
