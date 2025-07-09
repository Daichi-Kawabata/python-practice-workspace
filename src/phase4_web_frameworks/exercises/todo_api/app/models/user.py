from sqlalchemy.orm.properties import MappedColumn
from database import Base
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, mapped_column



class User(Base):
    __tablename__ = "users"
    
    # カラム定義
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, index=True)
    username: MappedColumn[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: MappedColumn[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: MappedColumn[str] = mapped_column(String, nullable=False)
    is_active: MappedColumn[bool] = mapped_column(Boolean, default=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: MappedColumn[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # リレーション
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")