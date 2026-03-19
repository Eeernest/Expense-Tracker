from tests.fixtures.user_fixture import user_repo, user_data, user_list
from tests.test_database import db_session

from app.models.user_model import UserRole

def test_create_user_repo_success(user_repo, user_data):
  created_user = user_repo.save(user_data)

  assert created_user.id is not None
  assert created_user.username == "user1"
  assert created_user.role == UserRole.user

def test_check_username(user_repo, user_data):
  user_repo.save(user_data)

  found_user = user_repo.check_username(user_data.username)

  assert found_user is not None
  assert found_user.username == "user1"

def test_check_email(user_repo, user_data):
  user_repo.save(user_data)

  found_email = user_repo.check_email(user_data.email)

  assert found_email is not None
  assert found_email.email == "user1@example.com"

def test_view_all_success(user_repo, user_list):
  result = user_repo.view_all(0, 10)

  assert len(result) == 2

def test_view_all_role_filter(user_repo, user_list):
  result = user_repo.view_all(0, 10, UserRole.user)

  assert len(result) == 1
  assert all(user.id == 1 for user in result)
  assert all(user.role == UserRole.user for user in result)
  assert all(user.role != UserRole.admin for user in result)

def test_view_all_offset(user_repo, user_list):
  result = user_repo.view_all(1, 10)

  assert len(result) == 1

def test_view_all_limit(user_repo, user_list):
  result = user_repo.view_all(0, 1)

  assert len(result) == 1