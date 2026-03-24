from app.models.expense_model import Expense, ExpenseCategory
from app.schemas.expense_schema import ExpenseEdit

from tests.fixtures.expense_fixture import expense_data, create_data, user, repo, exp_service, category, date, edit
import pytest
from fastapi import HTTPException

def test_add_expense_success(repo, expense_data, exp_service, category, create_data, user):
  repo.save.return_value = expense_data

  result = exp_service.add_expense(category, create_data, user)

  assert result.description == "rent"
  assert result.category == ExpenseCategory.housing
  assert result.user_id is not None

  repo.save.assert_called_once()

def test_no_description(repo, exp_service, category, user):
  data = Expense(
    description=None,
    amount=1000
  )

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Description" in str(exc.value)

  repo.save.assert_not_called()

def test_no_ammount(exp_service, category, user, repo):
  data = Expense(
    description="rent",
    amount=None
  )

  with pytest.raises(HTTPException) as exc:
    exp_service.add_expense(category, data, user)

  assert exc.value.status_code == 422
  assert "Amount" in str(exc.value)

  repo.save.assert_not_called()

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

def test_sum_expense_success(repo, date, exp_service, user):
  repo.sum_expense.return_value = 2000

  result = exp_service.sum_expense(user, date)

  assert result == 2000

  repo.sum_expense.assert_called_once()

def test_edit_success(repo, expense_data, exp_service, user, edit):
  repo.check_user_expense.return_value = expense_data
  repo.save.return_value = expense_data

  result = exp_service.edit(user, edit, "apples", 100, ExpenseCategory.food)

  assert result.description == "apples"
  assert result.amount == 100
  assert result.category == ExpenseCategory.food

  repo.check_user_expense.assert_called_once()
  repo.save.assert_called_once()

def test_edit_no_expense(repo, exp_service, user, edit):
  repo.check_user_expense.return_value = None
  
  with pytest.raises(HTTPException) as exc:
    exp_service.edit(user, edit, "apples", 100, ExpenseCategory.food)

  assert exc.value.status_code == 404
  assert "Expense" in str(exc.value)

  repo.check_user_expense.assert_called_once()

def test_edit_no_field(repo, expense_data, exp_service, user, edit):
  repo.check_user_expense.return_value = expense_data

  with pytest.raises(HTTPException) as exc:
    exp_service.edit(user, edit)

  assert exc.value.status_code == 422
  assert "field" in str(exc.value)

  repo.check_user_expense.assert_called_once()

def test_delete_expense_success(repo, expense_data, exp_service, user, edit):
  repo.check_user_expense.return_value = expense_data
  repo.delete_expense.return_value = {"message": "Expense deleted"}

  result = exp_service.delete_expense(user, edit)

  assert result == {"message": "Expense deleted"}

  repo.check_user_expense.assert_called_once()
  repo.delete_expense.assert_called_once()

def test_delete_expense_no_expense(repo, exp_service, user, edit):
  repo.check_user_expense.return_value = None
  
  with pytest.raises(HTTPException) as exc:
    exp_service.delete_expense(user, edit)

  assert exc.value.status_code == 404
  assert exc.value.detail == "Expense not found"

  repo.check_user_expense.assert_called_once()
  repo.delete_expense.assert_not_called()

def test_view_all_user_expenses_success(repo, expense_data, exp_service, category):
  repo.view_all_user_expenses.return_value = [expense_data, expense_data]

  result = exp_service.view_all_user_expenses(0, 10, category)

  assert len(result) == 2
  assert result[0].category == ExpenseCategory.housing

  repo.view_all_user_expenses.assert_called_once()

def test_view_all_user_expenses_empty_list(repo, exp_service):
  repo.view_all_user_expenses.return_value = []

  result = exp_service.view_all_user_expenses(0, 10)

  assert result == []

  repo.view_all_user_expenses.assert_called_once()

def test_view_user_expense_success(repo, expense_data, exp_service, category):
  repo.check_user_id.return_value = expense_data
  repo.view_user_expense.return_value = [expense_data, expense_data]

  result = exp_service.view_user_expense(1, 0, 10, category)

  assert len(result) == 2
  assert result[0].category == ExpenseCategory.housing

  repo.check_user_id.assert_called_once()
  repo.view_user_expense.assert_called_once()

def test_view_user_expense_empty_list(repo, expense_data, exp_service):
  repo.check_user_id.return_value = expense_data
  repo.view_user_expense.return_value = []

  result = exp_service.view_user_expense(1, 0, 10)

  assert result == []

  repo.check_user_id.assert_called_once()
  repo.view_user_expense.assert_called_once()

def test_view_user_expense_no_id(repo, exp_service):
  repo.check_user_id.return_value = None

  with pytest.raises(HTTPException) as exc:
    exp_service.view_user_expense(1, 0, 10)

  assert exc.value.status_code == 404
  assert exc.value.detail == "User ID not found"

  repo.check_user_id.assert_called_once()