from app.core.security import Security
from app.core.security import DUMMY_HASH
from app.core.config import Config
from app.repositories.auth_repository import AuthRepository
from app.schemas.token_schema import TokenBase

from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

class AuthService:
  def __init__(self, secure: Security, config: Config, repo: AuthRepository):
    self.secure = secure
    self.config = config
    self.repo = repo

  def _authenticate_user(self, username: str, password: str):
    user = self.repo.check_username(username)

    if not user:
      self.secure.verify_password(password, DUMMY_HASH)
      return False
    
    if not self.secure.verify_password(password, user.hashed_password):
      return False
    
    return user
  
  def _create_access_token(self, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
    
    else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = self.secure.encode_jwt(
      to_encode,
      self.config.SECRET_KEY,
      algorithm=self.config.ALGORITHM
    )

    return encoded_jwt
  
  def login(self, username: str, password: str) -> TokenBase:
    user = self._authenticate_user(username, password)

    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
      )
    
    access_token_expires = timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = self._create_access_token(
      data={"sub": str(user.id)},
      expires_delta=access_token_expires
    )

    return TokenBase(access_token=access_token, token_type="bearer")