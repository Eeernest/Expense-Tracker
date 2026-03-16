from tests.fixtures.expense_fixture import expense_repo, expense_data, expense_list, expense_dates
from tests.test_database import db_session

from app.models.expense_model import Expense, ExpenseCategory

from datetime import datetime, timedelta

def test_add_expense_success(expense_repo, expense_data):
  created_expense = expense_repo.add_expense(expense_data)

  assert created_expense.id is not None
  assert created_expense.description == "rent"
  assert created_expense.category == ExpenseCategory.housing

def test_view_all_success(expense_repo, expense_list):
  lists = expense_repo.view_all(1, 0, 10)

  assert len(lists) == 10
  assert all(exp.user_id == 1 for exp in lists)

def test_view_all_category(expense_repo, expense_list):
  category = ExpenseCategory.entertainment

  lists = expense_repo.view_all(1, 0, 10, category)

  assert len(lists) == 5
  assert all(exp.user_id == 1 for exp in lists)
  assert all(exp.category == ExpenseCategory.entertainment for exp in lists)
  assert all(exp.category != ExpenseCategory.housing for exp in lists)

def test_view_all_offset(expense_repo, expense_list):
  lists = expense_repo.view_all(1, 2, 10)

  assert len(lists) == 8

def test_view_all_limit(expense_repo, expense_list):
  lists = expense_repo.view_all(1, 0, 3)

  assert len(lists) == 3

def test_view_date_ninety_days(expense_repo, expense_dates):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)

  lists = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(lists) == 20

def test_view_date_thirty_days(expense_repo, expense_dates):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=30)

  lists = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(lists) == 15

def test_view_date_seven_days(expense_repo, expense_dates):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=7)

  lists = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(lists) == 10

def test_view_date_today(expense_repo, expense_dates):
  end_date = datetime(2026, 3, 1)
  start_date = end_date

  lists = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(lists) == 5

def test_view_date_category(expense_repo, expense_dates):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)
  category = ExpenseCategory.healthcare

  lists = expense_repo.view_date(1, start_date, end_date, 0, 100, category)

  assert len(lists) == 5
  assert all(exp.user_id == 1 for exp in lists)
  assert all(exp.category == ExpenseCategory.healthcare for exp in lists)
  assert all(exp.category != ExpenseCategory.housing for exp in lists)
  assert all(exp.category != ExpenseCategory.food for exp in lists)
  assert all(exp.category != ExpenseCategory.entertainment for exp in lists)