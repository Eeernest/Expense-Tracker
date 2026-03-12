from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import User

class PermitRepository:
  def __init__(self, session: Session):
    self.session = session

  def check_user_id(self, user_id: int) -> User | None:
    return self.session.execute(select(User).where(User.id == user_id)).scalars().first()