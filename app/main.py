from fastapi import FastAPI
from contextlib import contextmanager

from app.db.database import create_db_and_table
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.permit_router import router as permit_router

app = FastAPI()

@contextmanager
def lifespan(app: FastAPI):
  create_db_and_table()

@app.get("/")
def read_root():
  return {"message": "Hello World"}

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(permit_router)