from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token_schema import TokenBase
from app.dependencies.auth_dependency import AuthDep

router = APIRouter()

@router.post("/token", response_model=TokenBase)
async def auth_login(service: AuthDep, data: OAuth2PasswordRequestForm = Depends()):
  return service.login(data.username, data.password)