from app.models.expense_model import Expense, ExpenseCategory
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseBase
from app.repositories.expense_repository import ExpenseRepository

from fastapi import HTTPException

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

  def view_all(self, user_id: User, offset: int, limit: int) -> list[Expense]:
    return self.repo.view_all(user_id, offset, limit)