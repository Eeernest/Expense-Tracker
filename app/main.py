from fastapi import FastAPI

from app.db.database import create_db_and_table, SessionLocal
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.permit_router import router as permit_router
from app.routers.expense_router import router as expense_router
from app.core.middleware import LoggingMiddleware

from app.core.security import Security
from app.core.config import Config
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_table()

  db = SessionLocal()
  try:
    repo = UserRepository(db)
    service = UserService(Security(), Config(), repo)
    service.create_admin()
  finally:
    db.close()

@app.get("/")
def read_root():
  return {"message": "Hello World"}

app.add_middleware(LoggingMiddleware)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(permit_router)
app.include_router(expense_router)