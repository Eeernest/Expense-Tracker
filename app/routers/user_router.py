from fastapi import APIRouter, Query
from typing import Annotated

from app.schemas.user_schema import UserRead, UserCreate, UserAdminRead
from app.dependencies.user_dependency import UserDep
from app.dependencies.permit_dependency import CurrentAdminDep

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_data: UserCreate, service: UserDep):
  return service.create_account(user_data)

@router.get("/users", response_model=list[UserAdminRead])
def view_all(admin: CurrentAdminDep, service: UserDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
  return service.view_all(offset, limit)