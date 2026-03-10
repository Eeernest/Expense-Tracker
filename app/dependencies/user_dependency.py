from fastapi import Depends
from app.db.database import SessionDep
from app.core.security import Security
from app.core.config import Config
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from typing import Annotated

def get_user_service(session: SessionDep):
  secure = Security()
  config = Config()
  repo = UserRepository(session)

  return UserService(secure, config, repo)


UserDep = Annotated[UserService, Depends(get_user_service)]