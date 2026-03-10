import enum
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Column, Enum, DateTime
from app.db.database import Base

class UserRole(str, enum.Enum):
  user = "user"
  admin = "admin"

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False, index=True, unique=True)
  email = Column(String, nullable=True, index=True, unique=True)
  hashed_password = Column(String, nullable=False)
  role = Column(Enum(UserRole), default=UserRole.user)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))