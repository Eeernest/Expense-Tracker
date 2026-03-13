from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.expense_model import Expense

class ExpenseRepository:
  def __init__(self, session: Session):
    self.session = session

  def add_expense(self, expense: Expense) -> Expense:
    self.session.add(expense)
    self.session.commit()
    self.session.refresh(expense)

    return expense

  def view_all(self, user_id: int, offset: int, limit: int) -> list[Expense]:
    return self.session.execute(select(Expense).where(Expense.user_id == user_id).offset(offset).limit(limit)).scalars().all()