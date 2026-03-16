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
  lists = expense_repo.view_all(user_id, 0, 10)

  assert len(lists) == 10
  assert all(exp.user_id == user_id for exp in lists)

def test_view_all_category(expense_repo, expense_list):
  user_id = 1
  category = ExpenseCategory.housing

  lists = expense_repo.view_all(user_id, 0, 10, category)

  assert len(lists) == 5
  assert all(exp.user_id == user_id for exp in lists)
  assert all(exp.category == ExpenseCategory.housing for exp in lists)

def test_view_all_offset(expense_repo, expense_list):
  user_id = 1
  lists = expense_repo.view_all(user_id, 2, 10)

  assert len(lists) == 8

def test_view_all_limit(expense_repo, expense_list):
  user_id = 1
  lists = expense_repo.view_all(user_id, 0, 3)

  assert len(lists) == 3