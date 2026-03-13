from fastapi import Depends
from typing import Annotated

from app.db.database import SessionDep
from app.core.security import Security
from app.core.config import Config
from app.models.user_model import User
from app.repositories.permit_repository import PermitRepository
from app.services.permit_service import PermitService

def get_permit_service(session: SessionDep):
  secure = Security()
  config = Config()
  repo = PermitRepository(session)

  return PermitService(secure, config, repo)

PermitDep = Annotated[PermitService, Depends(get_permit_service)]

TokenDep = Annotated[str, Depends(Security.oauth2_scheme)]

def current_user(token: TokenDep, service: PermitDep) -> User:
  return service.get_current_user(token)

CurrentUserDep = Annotated[User, Depends(current_user)]