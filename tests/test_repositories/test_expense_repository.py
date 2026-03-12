from tests.fixtures.expense_fixture import expense_repo, expense_data
from tests.test_database import db_session

from app.models.expense_model import ExpenseCategory

def test_add_expense_success(expense_repo, expense_data):
  created_expense = expense_repo.add_expense(expense_data)

  assert created_expense.id is not None
  assert created_expense.description == "rent"
  assert created_expense.category == ExpenseCategory.housing