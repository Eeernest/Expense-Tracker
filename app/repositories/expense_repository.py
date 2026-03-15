from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.expense_model import Expense, ExpenseCategory
from app.schemas.expense_schema import ExpenseDate

from datetime import datetime

class ExpenseRepository:
  def __init__(self, session: Session):
    self.session = session

  def add_expense(self, expense: Expense) -> Expense:
    self.session.add(expense)
    self.session.commit()
    self.session.refresh(expense)

    return expense

  def view_all(self, user_id: int, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    statement = select(Expense).where(Expense.user_id == user_id).offset(offset).limit(limit)

    if category:
      statement = statement.where(Expense.category == category)

    return self.session.execute(statement).scalars().all()
  
  def view_date(self, user_id: int, start_date: datetime, end_date: datetime, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    statement = select(Expense).where(Expense.user_id == user_id, Expense.date >= start_date, Expense.date < end_date).offset(offset).limit(limit)

    if category:
      statement = statement.where(Expense.category == category)

    return self.session.execute(statement).scalars().all()