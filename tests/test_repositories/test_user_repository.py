from tests.fixtures.user_fixture import fx_repo, user_data
from tests.test_database import db_session

from app.repositories.user_repository import UserRepository
from app.models.user_model import User, UserRole

def test_create_user_repo(fx_repo, user_data):
  created_user = fx_repo.create_repo(user_data)

  assert created_user.id is not None
  assert created_user.username == "user1"
  assert created_user.role == UserRole.user

def test_check_username(fx_repo, user_data):
  fx_repo.create_repo(user_data)

  found_user = fx_repo.check_username(user_data.username)

  assert found_user is not None
  assert found_user.username == "user1"

def test_check_email(fx_repo, user_data):
  fx_repo.create_repo(user_data)

  found_email = fx_repo.check_email(user_data.email)

  assert found_email is not None
  assert found_email.email == "user1@example.com"