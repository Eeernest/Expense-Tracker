from app.models.expense_model import Expense, ExpenseCategory

from tests.fixtures.expense_fixture import expense_data, create_data, user, repo, exp_service
import pytest
from fastapi import HTTPException

def test_add_expense_success(expense_data, create_data, user, repo, exp_service):
  repo.add_expense.return_value = expense_data
  category = ExpenseCategory.housing

  added_exp = exp_service.add_expense(category, create_data, user)

  assert added_exp.description == "rent"
  assert added_exp.category == ExpenseCategory.housing
  assert added_exp.user_id is not None

  repo.add_expense.assert_called_once()

def test_no_description(repo, user, exp_service):
  data = Expense(
    description=None,
    amount=1000
  )

  category = ExpenseCategory.housing

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Description" in str(exc.value)

  repo.add_expense.assert_not_called()

def test_no_ammount(repo, user, exp_service):
  data = Expense(
    description="rent",
    amount=None
  )

  category = ExpenseCategory.housing

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Amount" in str(exc.value)

  repo.add_expense.assert_not_called()