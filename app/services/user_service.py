from app.core.security import Security
from app.core.config import Config
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserCreate, UserRead
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException

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

    return self.repo.create_repo(new_account)