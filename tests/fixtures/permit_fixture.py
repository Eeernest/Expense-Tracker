from unittest.mock import Mock
import pytest

from app.repositories.permit_repository import PermitRepository
from app.repositories.user_repository import UserRepository
from app.services.permit_service import PermitService
from app.models.user_model import User, UserRole

from tests.test_database import db_session



# repository

@pytest.fixture
def permit_repo(db_session):
  return PermitRepository(db_session)

@pytest.fixture
def user_data():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    role=UserRole.user
  )

@pytest.fixture
def created_user(db_session, user_data):
  repo = UserRepository(db_session)
  return repo.create_repo(user_data)

# service

@pytest.fixture
def secure():
  return Mock()

@pytest.fixture
def config():
  cfg = Mock()
  cfg.SECRET_KEY = "secret"
  cfg.ALGORITHM = "HS256"

  return cfg


@pytest.fixture
def repo():
  return Mock()

@pytest.fixture
def permit_service(secure, config, repo):
  return PermitService(secure, config, repo)