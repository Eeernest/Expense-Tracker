import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:
  SECRET_KEY = os.getenv("SECRET_KEY")
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
  ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

  DATABASE_URL = f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT", 5432)}/{os.getenv("POSTGRES_DB")}"