from app.models.expense_model import Expense, ExpenseCategory
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseBase, ExpenseDate
from app.repositories.expense_repository import ExpenseRepository

from fastapi import HTTPException
from datetime import datetime, timedelta

class ExpenseService:
  def __init__(self, repo: ExpenseRepository):
    self.repo = repo

  def add_expense(self, category: ExpenseCategory, exp_data: ExpenseBase, user: User) -> Expense:
    if exp_data.description is None:
      raise HTTPException(status_code=422, detail="Description is required")
    
    if exp_data.amount is None:
      raise HTTPException(status_code=422, detail="Amount is required")

    new_expense = Expense(
      description=exp_data.description,
      amount=exp_data.amount,
      category=category,
      user_id=user.id
    )

    return self.repo.add_expense(new_expense)

  def view_all(self, user: User, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    return self.repo.view_all(user.id, offset, limit, category)
  
  def view_date(self, user: User, date: ExpenseDate, offset: int, limit: int, category: ExpenseCategory | None = None) -> list[Expense]:
    date_now = datetime.now()

    if date == ExpenseDate.today:
      start_date = datetime(date_now.year, date_now.month, date_now.day)
      end_date = start_date + timedelta(days=1)

    elif date == ExpenseDate.seven_days:
      start_date = date_now - timedelta(days=7)
      end_date = date_now

    elif date == ExpenseDate.thirty_days:
      start_date = date_now - timedelta(days=30)
      end_date = date_now

    elif date == ExpenseDate.ninety_days:
      start_date = date_now - timedelta(days=90)
      end_date = date_now

    return self.repo.view_date(user.id, start_date, end_date, offset, limit, category)