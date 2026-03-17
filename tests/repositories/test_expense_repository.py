from tests.fixtures.expense_fixture import expense_repo, expense_data, expense_list
from tests.test_database import db_session

from app.models.expense_model import Expense, ExpenseCategory

from datetime import datetime, timedelta

def test_add_expense_success(expense_repo, expense_data):
  ressult = expense_repo.save(expense_data)

  assert ressult.id is not None
  assert ressult.description == "rent"
  assert ressult.category == ExpenseCategory.housing

def test_view_all_success(expense_repo, expense_list):
  ressult = expense_repo.view_all(1, 0, 10)

  assert len(ressult) == 10
  assert all(exp.user_id == 1 for exp in ressult)

def test_view_all_category(expense_repo, expense_list):
  category = ExpenseCategory.entertainment

  ressult = expense_repo.view_all(1, 0, 10, category)

  assert len(ressult) == 5
  assert all(exp.user_id == 1 for exp in ressult)
  assert all(exp.category == ExpenseCategory.entertainment for exp in ressult)
  assert all(exp.category != ExpenseCategory.housing for exp in ressult)

def test_view_all_offset(expense_repo, expense_list):
  ressult = expense_repo.view_all(1, 2, 18)

  assert len(ressult) == 18

def test_view_all_limit(expense_repo, expense_list):
  ressult = expense_repo.view_all(1, 0, 3)

  assert len(ressult) == 3

def test_view_date_ninety_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)

  ressult = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(ressult) == 20

def test_view_date_thirty_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=30)

  ressult = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(ressult) == 15

def test_view_date_seven_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=7)

  ressult = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(ressult) == 10

def test_view_date_today(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date

  ressult = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(ressult) == 5

def test_view_date_category(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)
  category = ExpenseCategory.healthcare

  ressult = expense_repo.view_date(1, start_date, end_date, 0, 100, category)

  assert len(ressult) == 5
  assert all(exp.user_id == 1 for exp in ressult)
  assert all(exp.category == ExpenseCategory.healthcare for exp in ressult)
  assert all(exp.category != ExpenseCategory.housing for exp in ressult)
  assert all(exp.category != ExpenseCategory.food for exp in ressult)
  assert all(exp.category != ExpenseCategory.entertainment for exp in ressult)

def test_check_user_expense_success(expense_repo, expense_data):
  expense_repo.save(expense_data)
  result = expense_repo.check_user_expense(expense_data.user_id, expense_data.id)

  assert result.user_id == 1
  assert result.id == 1