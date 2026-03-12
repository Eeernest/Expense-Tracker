import pytest

from app.repositories.expense_repository import ExpenseRepository
from app.models.expense_model import Expense, ExpenseCategory

from tests.test_database import db_session

# repository

@pytest.fixture
def expense_repo(db_session):
  return ExpenseRepository(db_session)

@pytest.fixture
def expense_data():
  return Expense(
    description="rent",
    amount=1000,
    category=ExpenseCategory.housing,
    user_id=1
  )