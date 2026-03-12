from unittest.mock import Mock
import pytest

from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserCreate

from tests.test_database import db_session


#  repository


@pytest.fixture
def auth_repo(db_session):
  return AuthRepository(db_session)

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
  cfg = Mock()
  cfg.SECRET_KEY = "secret"
  cfg.ALGORITHM = "HS256"
  cfg.ACCESS_TOKEN_EXPIRE_MINUTES = 30

  return cfg

@pytest.fixture
def repo():
  return Mock()

@pytest.fixture
def auth_service(secure, config, repo):
  return AuthService(secure, config, repo)