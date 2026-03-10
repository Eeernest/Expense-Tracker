import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:
  SECRET_KEY = os.getenv("SECRET_KEY")
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
  ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

  POSTGRES_USER = os.getenv("POSTGRES_USER")
  POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
  POSTGRES_DB = os.getenv("POSTGRES_DB")
  POSTGRES_HOST = os.getenv("POSTGRES_HOST")
  POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

  DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"