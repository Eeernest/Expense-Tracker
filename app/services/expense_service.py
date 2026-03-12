from app.models.expense_model import Expense, ExpenseCategory
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseCreate
from app.repositories.expense_repository import ExpenseRepository

class ExpenseService:
  def __init__(self, repo: ExpenseRepository):
    self.repo = repo

  def add_expense(self, exp_data: ExpenseCreate, user: User) -> Expense:
    new_expense = Expense(
      description=exp_data.description,
      amount=exp_data.amount,
      category=exp_data.category,
      user_id=user.id
    )

    return self.repo.add_expense(new_expense)