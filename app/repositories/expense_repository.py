from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.expense_model import Expense, ExpenseCategory

from datetime import datetime

class ExpenseRepository:
  def __init__(self, session: Session):
    self.session = session

  def check_user_expense(self, user_id: int, expense_id: int) -> Expense | None:
    return self.session.execute(select(Expense).where(Expense.user_id == user_id, Expense.id == expense_id)).scalar_one_or_none()
  
  def check_user_id(self, user_id: int) -> Expense | None:
    return self.session.execute(select(Expense).where(Expense.user_id == user_id)).scalar_one_or_none()

  def save(self, expense: Expense) -> Expense:
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
    statement = select(Expense).where(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).offset(offset).limit(limit)

    if category:
      statement = statement.where(Expense.category == category)

    return self.session.execute(statement).scalars().all()

  def sum_expense(self, user_id: int, start_date: datetime, end_date: datetime, category: ExpenseCategory | None = None) -> float:
    statement = select(func.sum(Expense.amount)).where(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date)

    if category:
      statement = statement.where(Expense.category == category)

    return self.session.execute(statement).scalar() or 0.0

  def delete_expense(self, expense: Expense):
    self.session.delete(expense)
    self.session.commit()

    return {"message": "Expense deleted"}

  def view_all_user_expenses(self, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    statement = select(Expense).offset(offset).limit(limit)

    if category is not None:
      statement = statement.where(Expense.category == category)
    
    return self.session.execute(statement).scalars().all()

  def view_user_expense(self, user_id: int, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    statement = select(Expense).where(Expense.user_id == user_id).offset(offset).limit(limit)

    if category is not None:
      statement = statement.where(Expense.category == category)

    return self.session.execute(statement).scalars().all()