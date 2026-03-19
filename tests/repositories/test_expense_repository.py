from tests.fixtures.expense_fixture import expense_repo, expense_data, expense_list
from tests.test_database import db_session

from app.models.expense_model import Expense, ExpenseCategory

from datetime import datetime, timedelta

def test_add_expense_success(expense_repo, expense_data):
  result = expense_repo.save(expense_data)

  assert result.id is not None
  assert result.description == "rent"
  assert result.category == ExpenseCategory.housing

def test_view_all_success(expense_repo, expense_list):
  result = expense_repo.view_all(1, 0, 10)

  assert len(result) == 10
  assert all(exp.user_id == 1 for exp in result)

def test_view_all_category(expense_repo, expense_list):
  category = ExpenseCategory.entertainment

  result = expense_repo.view_all(1, 0, 10, category)

  assert len(result) == 5
  assert all(exp.user_id == 1 for exp in result)
  assert all(exp.category == ExpenseCategory.entertainment for exp in result)
  assert all(exp.category != ExpenseCategory.housing for exp in result)

def test_view_all_offset(expense_repo, expense_list):
  result = expense_repo.view_all(1, 2, 18)

  assert len(result) == 18

def test_view_all_limit(expense_repo, expense_list):
  result = expense_repo.view_all(1, 0, 3)

  assert len(result) == 3

def test_view_date_ninety_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)

  result = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(result) == 20

def test_view_date_thirty_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=30)

  result = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(result) == 15

def test_view_date_seven_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=7)

  result = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(result) == 10

def test_view_date_today(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date

  result = expense_repo.view_date(1, start_date, end_date, 0, 100)

  assert len(result) == 5

def test_view_date_category(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)
  category = ExpenseCategory.healthcare

  result = expense_repo.view_date(1, start_date, end_date, 0, 100, category)

  assert len(result) == 5
  assert all(exp.user_id == 1 for exp in result)
  assert all(exp.category == ExpenseCategory.healthcare for exp in result)
  assert all(exp.category != ExpenseCategory.housing for exp in result)
  assert all(exp.category != ExpenseCategory.food for exp in result)
  assert all(exp.category != ExpenseCategory.entertainment for exp in result)

def test_check_user_expense_success(expense_repo, expense_data):
  expense_repo.save(expense_data)
  result = expense_repo.check_user_expense(expense_data.user_id, expense_data.id)

  assert result.user_id == 1
  assert result.id == 1

def test_sum_expense_ninety_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)

  result = expense_repo.sum_expense(1, start_date, end_date)

  assert result == 13500

def test_sum_expense_thirty_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=30)

  result = expense_repo.sum_expense(1, start_date, end_date)

  assert result == 8500

def test_sum_expense_seven_days(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=7)

  result = expense_repo.sum_expense(1, start_date, end_date)

  assert result == 6000

def test_sum_expense_no_expenses(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)
  category = ExpenseCategory.transportation

  result = expense_repo.sum_expense(1, start_date, end_date, category)

  assert result == 0

def test_sum_expense_today(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date

  result = expense_repo.sum_expense(1, start_date, end_date)

  assert result == 5000

def test_sum_expense_category(expense_repo, expense_list):
  end_date = datetime(2026, 3, 1)
  start_date = end_date - timedelta(days=90)
  category = ExpenseCategory.entertainment

  result = expense_repo.sum_expense(1, start_date, end_date, category)

  assert result == 1000

def test_delete_expense_success(expense_repo, expense_data):
  data = expense_repo.save(expense_data)
  result = expense_repo.delete_expense(data)

  assert result == {"message": "Expense deleted"}

def test_view_all_user_expenses_success(expense_repo, expense_list):
  result = expense_repo.view_all_user_expenses(0, 10, ExpenseCategory.housing)

  assert len(result) == 5
  assert all(exp.category == ExpenseCategory.housing for exp in result)

def test_view_all_user_expenses_offset(expense_repo, expense_list):
  result = expense_repo.view_all_user_expenses(2, 20)

  assert len(result) == 18

def test_view_all_user_expenses_limit(expense_repo, expense_list):
  result = expense_repo.view_all_user_expenses(0, 5)

  assert len(result) == 5