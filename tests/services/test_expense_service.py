from app.models.expense_model import Expense, ExpenseCategory

from tests.fixtures.expense_fixture import expense_data, create_data, user, repo, exp_service, category, date
import pytest
from fastapi import HTTPException

def test_add_expense_success(repo, expense_data, exp_service, category, create_data, user):
  repo.add_expense.return_value = expense_data

  result = exp_service.add_expense(category, create_data, user)

  assert result.description == "rent"
  assert result.category == ExpenseCategory.housing
  assert result.user_id is not None

  repo.add_expense.assert_called_once()

def test_no_description(repo, exp_service, category, user):
  data = Expense(
    description=None,
    amount=1000
  )

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Description" in str(exc.value)

  repo.add_expense.assert_not_called()

def test_no_ammount(exp_service, category, user, repo):
  data = Expense(
    description="rent",
    amount=None
  )

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Amount" in str(exc.value)

  repo.add_expense.assert_not_called()

def test_view_all_success(repo, expense_data, exp_service, user):
  repo.view_all.return_value = [expense_data, expense_data]

  result = exp_service.view_all(user, 0, 2)

  assert len(result) == 2
  assert result[0].user_id == 1
  assert result[0].description == "rent"

  repo.view_all.assert_called_once()

def test_view_all_categoty(repo, expense_data, exp_service, user, category):
  repo.view_all.return_value = [expense_data]

  result = exp_service.view_all(user, 0, 1, category)

  assert len(result) == 1
  assert result[0].category == ExpenseCategory.housing

  repo.view_all.assert_called_once()

def test_view_all_empty_list(repo, exp_service, user):
  repo.view_all.return_value = []

  result = exp_service.view_all(user, 0, 2)

  assert result == []

  repo.view_all.assert_called_once()

def test_view_date_success(repo, date, expense_data, exp_service, user):
  repo.view_date.return_value = [expense_data]

  result = exp_service.view_date(user, date, 0, 10)

  assert len(result) == 1
  assert result[0].category == ExpenseCategory.housing

  repo.view_date.assert_called_once()

def test_view_empty_list(repo, date, exp_service, user):
  repo.view_date.return_value = []

  result = exp_service.view_date(user, date, 0, 10)

  assert result == []

  repo.view_date.assert_called_once()