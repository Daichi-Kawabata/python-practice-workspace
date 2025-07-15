from sqlalchemy.orm.properties import MappedColumn
from app.database import Base
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column


class Task(Base):
    __tablename__ = "tasks"

    id: MappedColumn[int] = mapped_column(
        Integer, primary_key=True, index=True)
    title: MappedColumn[str] = mapped_column(String, nullable=False)
    description: MappedColumn[str] = mapped_column(Text, nullable=True)
    completed: MappedColumn[bool] = mapped_column(Boolean, default=False)
    priority: MappedColumn[str] = mapped_column(
        String, default="medium")  # low, medium, high
    due_date: MappedColumn[datetime] = mapped_column(DateTime, nullable=True)
    user_id: MappedColumn[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーション
    owner = relationship("User", back_populates="tasks")
