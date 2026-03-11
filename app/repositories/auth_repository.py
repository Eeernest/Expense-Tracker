from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import User

class AuthRepository:
  def __init__(self, session: Session):
    self.session = session

  def check_username(self, username: str) -> User | None:
    return self.session.execute(select(User).where(User.username == username)).scalars().first()