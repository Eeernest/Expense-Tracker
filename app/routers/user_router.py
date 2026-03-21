from fastapi import APIRouter, Query
from typing import Annotated

from app.models.user_model import UserRole
from app.schemas.user_schema import UserRead, UserCreate, UserAdminRead
from app.dependencies.user_dependency import UserDep
from app.dependencies.permit_dependency import CurrentAdminDep

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_data: UserCreate, service: UserDep):
  return service.create_account(user_data)

@router.get("/users", response_model=list[UserAdminRead])
def view_all(
  admin: CurrentAdminDep,
  service: UserDep,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
  role: UserRole | None = None
):
  return service.view_all(offset, limit, role)

@router.patch("/users/update", response_model=UserAdminRead)
def edit_role(
  admin: CurrentAdminDep,
  service: UserDep,
  user_id: int,
  role: UserRole
):
  return service.edit_role(user_id, role)

@router.delete("/users/delete")
def delete_user(
  admin: CurrentAdminDep,
  service: UserDep,
  user_id: int
):
  return service.delete_user(user_id)

@router.patch("/users/status", response_model=UserAdminRead)
def update_user_status(
  admin: CurrentAdminDep,
  service: UserDep,
  user_id: int,
  status: bool
):
  return service.update_user_status(user_id, status)