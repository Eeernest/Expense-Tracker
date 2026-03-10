from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import User

class UserRepository:
  def __init__(self, session: Session):
    self.session = session

  def check_username(self, username: str) -> User | None:
    return self.session.execute(select(User).where(User.username == username)).scalars().first()
  
  def check_email(self, email: str) -> User | None:
    return self.session.execute(select(User).where(User.email == email)).scalars().first()
  
  def create_repo(self, user: User) -> User:
    self.session.add(user)
    self.session.commit()
    self.session.refresh(user)
    return user