from app.models.expense_model import ExpenseCategory

from tests.fixtures.expense_fixture import expense_data, create_data, user, repo, exp_service

def test_add_expense_success(expense_data, create_data, user, repo, exp_service):
  repo.add_expense.return_value = expense_data

  added_exp = exp_service.add_expense(create_data, user)

  assert added_exp.description == "rent"
  assert added_exp.category == ExpenseCategory.housing
  assert added_exp.user_id is not None

  repo.add_expense.assert_called_once()