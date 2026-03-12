from unittest.mock import Mock
import pytest

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserCreate

from tests.test_database import db_session

# repository

@pytest.fixture
def user_repo(db_session):
  return UserRepository(db_session)

@pytest.fixture
def user_data():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    role=UserRole.user
  )

# service

@pytest.fixture
def create_data():
  return UserCreate(
    username="user1",
    email="user1@example.com",
    password="Password123",
    role=UserRole.user
  )

@pytest.fixture
def secure():
  return Mock()

@pytest.fixture
def config():
  return Mock()

@pytest.fixture
def repo():
  return Mock()

@pytest.fixture
def user_service(secure, config, repo):
  return UserService(secure, config, repo)