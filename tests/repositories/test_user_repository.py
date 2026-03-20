from tests.fixtures.user_fixture import user_repo, saved_data, user_data, user_list
from tests.test_database import db_session

from app.models.user_model import UserRole

def test_save(user_repo, saved_data):
  created_user = saved_data

  assert created_user.id == saved_data.id
  assert created_user.username == saved_data.username
  assert created_user.role == saved_data.role

def test_check(user_repo, saved_data):
  found_user = user_repo.check_username(saved_data.username)

  assert found_user.id == saved_data.id
  assert found_user.username == saved_data.username

def test_check_email(user_repo, saved_data):
  found_email = user_repo.check_email(saved_data.email)

  assert found_email.id == saved_data.id
  assert found_email.email == saved_data.email

def test_check_user_id(user_repo, saved_data):
  result = user_repo.check_user_id(saved_data.id)

  assert result.id == saved_data.id

def test_view_all(user_repo, user_list):
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

def test_delete_user(user_repo, saved_data):
  result = user_repo.delete_user(saved_data)

  assert result == {"message": "User deleted"}