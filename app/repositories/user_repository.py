from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import User, UserRole

class UserRepository:
  def __init__(self, session: Session):
    self.session = session

  def check_username(self, username: str) -> User | None:
    return self.session.execute(select(User).where(User.username == username)).scalars().first()
  
  def check_email(self, email: str) -> User | None:
    return self.session.execute(select(User).where(User.email == email)).scalars().first()
  
  def check_user_id(self, user_id: int) -> User | None:
    return self.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
  
  def save(self, user: User) -> User:
    self.session.add(user)
    self.session.commit()
    self.session.refresh(user)
    return user

  def view_all(self, offset: int, limit: int, role: UserRole | None = None) -> list[User]:
    statement = select(User).offset(offset).limit(limit)

    if role is not None:
      statement = statement.where(User.role == role)

    return self.session.execute(statement).scalars().all()