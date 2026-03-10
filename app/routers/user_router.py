from fastapi import APIRouter
from app.schemas.user_schema import UserRead, UserCreate
from app.dependencies.user_dependency import UserDep

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_data: UserCreate, service: UserDep):
  return service.create_account(user_data)