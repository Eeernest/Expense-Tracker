from tests.fixtures.expense_fixture import expense_repo, expense_data, expense_list
from tests.test_database import db_session

from app.models.expense_model import Expense, ExpenseCategory

def test_add_expense_success(expense_repo, expense_data):
  created_expense = expense_repo.add_expense(expense_data)

  assert created_expense.id is not None
  assert created_expense.description == "rent"
  assert created_expense.category == ExpenseCategory.housing

def test_view_all_success(expense_repo, expense_list):
  user_id = 1
  list = expense_repo.view_all(user_id, 0, 10)

  assert len(list) == 6

def test_view_all_offset(expense_repo, expense_list):
  user_id = 1
  expense_list = expense_repo.view_all(user_id, 2, 10)

  assert len(expense_list) == 4

def test_view_all_limit(expense_repo, expense_list):
  user_id = 1
  expense_list = expense_repo.view_all(user_id, 0, 3)

  assert len(expense_list) == 3