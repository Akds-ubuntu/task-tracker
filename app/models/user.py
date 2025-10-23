from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    token_version = Column(Integer, default=0)
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
