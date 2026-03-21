from app.core.security import Security
from app.core.config import Config
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserCreate
from app.repositories.user_repository import UserRepository

import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv(".env")

class UserService:
  def __init__(self, secure: Security, config: Config, repo: UserRepository):
    self.secure = secure
    self.config = config
    self.repo = repo

  def create_account(self, user: UserCreate) -> User:
    if self.repo.check_username(user.username):
      raise HTTPException(status_code=409, detail="Username is already in use")
    
    if self.repo.check_email(user.email):
      raise HTTPException(status_code=409, detail="Email is already in use")
    
    hashed_password = self.secure.get_password_hash(user.password)

    new_account = User(
      username=user.username,
      email=user.email,
      hashed_password=hashed_password,
      role=UserRole.user
    )

    return self.repo.save(new_account)
  
  def create_admin(self):
    admin_username = os.getenv("ADMIN_USERNAME")

    existing_username = self.repo.check_username(admin_username)

    if existing_username is not None:
      return

    hashed_password = self.secure.get_password_hash(os.getenv("ADMIN_PASSWORD"))

    first_admin = User(
      username=admin_username,
      hashed_password=hashed_password,
      role=UserRole.admin
    )

    return self.repo.save(first_admin)
  
  def view_all(self, offset: int, limit: int, role: UserRole | None = None) -> list[User]:
    return self.repo.view_all(offset, limit, role)

  def edit_role(self, user_id: int, role: UserRole) -> User:
    edited_user = self.repo.check_user_id(user_id)

    if edited_user is None:
      raise HTTPException(status_code=404, detail="User ID not found")
    
    if edited_user.role == role:
      raise HTTPException(status_code=409, detail="User already has this role")
    
    edited_user.role = role

    return self.repo.save(edited_user)
  
  def delete_user(self, user_id: int):
    user = self.repo.check_user_id(user_id)

    if user is None:
      raise HTTPException(status_code=404, detail="User ID not found")
    
    return self.repo.delete_user(user)

  def update_user_status(self, user_id: int, status: bool) -> User:
    user = self.repo.check_user_id(user_id)

    if user is None:
      raise HTTPException(status_code=404, detail="User ID not found")
    
    if user.is_active == status:
      raise HTTPException(status_code=409, detail="User already has this status")
    
    user.is_active = status

    return self.repo.save(user)