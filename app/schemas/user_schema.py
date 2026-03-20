from pydantic import BaseModel, field_validator, EmailStr, ConfigDict
import re
from datetime import datetime
from typing import Optional

from app.models.user_model import UserRole

class UserBase(BaseModel):
  username: str
  email: Optional[EmailStr]

class UserCreate(UserBase):
  password: str

  @field_validator("password")
  def strong_password(cls, v):
    if len(v) < 8:
      raise ValueError("Password should have at least 8 characters")
    
    if not re.search(r"[A-Z]", v):
      raise ValueError("Password should have at least one big letter")
    
    if not re.search(r"\d", v):
      raise ValueError("Password chould have at least one number")
    
    return v

class UserRead(UserBase):
  id: int

  model_config = ConfigDict(from_attributes=True)

class UserAdminRead(UserRead):
  role: UserRole
  created_at: datetime
  updated_at: datetime
  is_active: bool

  model_config = ConfigDict(from_attributes=True)