"""SQLAlchemy model for file metadata storage"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.database import Base


class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    name = Column(String)
    path = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())