import pytest
from unittest.mock import Mock

from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.models.expense_model import Expense, ExpenseCategory
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseBase, ExpenseDate

from tests.test_database import db_session

from datetime import datetime, timedelta

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

@pytest.fixture
def expense_list(expense_repo):
  expenses = []

  base_date = datetime(2026, 3, 1)

  for i in range(5):
    expense = expense_repo.add_expense(
      Expense(
        description="rent",
        amount=1000,
        category=ExpenseCategory.housing,
        date=base_date - timedelta(days=90),
        user_id=1
      )
    )

    expenses.append(expense)

    expense = expense_repo.add_expense(
      Expense(
        description="food",
        amount=500,
        category=ExpenseCategory.food,
        date=base_date - timedelta(days=30),
        user_id=1
      )
    )

    expenses.append(expense)

    expense = expense_repo.add_expense(
      Expense(
        description="dinner",
        amount=200,
        category=ExpenseCategory.entertainment,
        date=base_date - timedelta(days=7),
        user_id=1
      )
    )

    expenses.append(expense)

    expense = expense_repo.add_expense(
      Expense(
        description="dentist",
        amount=1000,
        category=ExpenseCategory.healthcare,
        date=base_date,
        user_id=1
      )
    )

    expenses.append(expense)

  return expenses

# service

@pytest.fixture
def create_data():
  return ExpenseBase(
     description="rent",
     amount=1000
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

@pytest.fixture
def category():
  return ExpenseCategory.housing

@pytest.fixture
def date():
  return ExpenseDate.ninety_days