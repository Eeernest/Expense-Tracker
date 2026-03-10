from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from app.core.config import Config

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

class Base(DeclarativeBase):
  pass

def create_db_and_table():
  Base.metadata.create_all(bind=engine)

def get_session():
  db = SessionLocal()

  try:
    yield db
  
  finally:
    db.close()

SessionDep = Annotated[Session, Depends(get_session)]