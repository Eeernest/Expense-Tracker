from app.core.security import Security
from app.schemas.user_schema import UserRead
from app.dependencies.permit_dependency import PermitDep

from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/users/me", response_model=UserRead)
def read_user_me(service: PermitDep, token: str = Depends(Security.oauth2_scheme)):
  return service.get_current_user(token)