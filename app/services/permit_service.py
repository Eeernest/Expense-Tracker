from app.core.security import Security
from app.core.config import Config
from app.repositories.permit_repository import PermitRepository
from app.schemas.token_schema import TokenData

from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError

class PermitService:
  def __init__(self, secure: Security, config: Config, repo: PermitRepository):
    self.secure = secure
    self.config = config
    self.repo = repo

  def get_current_user(self, token: str):
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"}
    )

    try:
      payload = self.secure.decode_jwt(token, self.config.SECRET_KEY, self.config.ALGORITHM)

      user_id = payload.get("sub")

      if user_id is None:
        raise credentials_exception
      
      token_data = TokenData(user_id=user_id)

    except InvalidTokenError:
      raise credentials_exception
    
    user = self.repo.check_user_id(int(token_data.user_id))

    if user is None:
      raise credentials_exception
    
    return user