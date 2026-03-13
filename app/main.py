from fastapi import FastAPI

from app.db.database import create_db_and_table
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.permit_router import router as permit_router
from app.routers.expense_router import router as expense_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
  create_db_and_table()

@app.get("/")
def read_root():
  return {"message": "Hello World"}

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(permit_router)
app.include_router(expense_router)