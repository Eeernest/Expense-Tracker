from fastapi import Depends
from typing import Annotated

from app.db.database import SessionDep
from app.core.security import Security
from app.core.config import Config
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService

def get_auth_service(session: SessionDep):
  secure = Security()
  config = Config()
  repo = AuthRepository(session)

  return AuthService(secure, config, repo)

AuthDep = Annotated[AuthService, Depends(get_auth_service)]