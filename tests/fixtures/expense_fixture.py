import pytest
from unittest.mock import Mock

from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.models.expense_model import Expense, ExpenseCategory
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseCreate

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

# service

@pytest.fixture
def create_data():
  return ExpenseCreate(
     description="rent",
     amount=1000,
     category=ExpenseCategory.housing,
     user_id=1
  )

@pytest.fixture
def user():
  return User(
    id=1
  )

@pytest.fixture
def repo():
  return Mock()

@pytest.fixture
def exp_service(repo):
  return ExpenseService(repo)