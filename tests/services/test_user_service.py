from app.models.user_model import UserRole
from app.schemas.user_schema import UserCreate

from tests.fixtures.user_fixture import create_data, secure, config, repo, user_service, user_data

import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from pydantic import ValidationError

def test_save_success(secure, repo, user_service, create_data):
  repo.check_username.return_value = None
  repo.check_email.return_value = None

  secure.get_password_hash.return_value = "Hashedpassword123"

  repo.save.return_value = Mock(
    username="user1",
    email="user1@example.com",
    role=UserRole.user
  )

  created_user = user_service.create_account(create_data)

  assert created_user.username == "user1"
  assert created_user.role == UserRole.user

  secure.get_password_hash.assert_called_once()
  repo.save.assert_called_once()

def test_username_failure(repo, user_service, create_data):
  repo.check_username.return_value = Mock()

  with pytest.raises(HTTPException) as exc:
    user_service.create_account(create_data)

  assert exc.value.status_code == 409
  repo.save.assert_not_called()

def test_email_failure(repo, user_service, create_data):
  repo.check_email.return_value = Mock()

  with pytest.raises(HTTPException) as exc:
    user_service.create_account(create_data)

  assert exc.value.status_code == 409
  repo.create_repo.assert_not_called()

def test_password_letter_failure():
  with pytest.raises(ValidationError) as exc:
    user_data = UserCreate(
      username="user1",
      email="user1@example.com",
      password="password123"
    )

  assert "Password" in str(exc.value)

def test_password_number_failure():
  with pytest.raises(ValidationError) as exc:
    user_data = UserCreate(
      username="user1",
      email="user1@example.com",
      password="Passwordtest"
    )

  assert "Password" in str(exc.value)

def test_password_length_failure():
  with pytest.raises(ValidationError) as exc:
    user_data = UserCreate(
      username="user1",
      email="user1@example.com",
      password="Pas1"
    )

  assert "Password" in str(exc.value)

def test_view_all_success(repo, user_data, user_service):
  repo.view_all.return_value = [user_data]

  result = user_service.view_all(0, 10, UserRole.user)

  assert len(result) == 1
  assert result[0].role == user_data.role
  assert result[0].role != UserRole.admin

  repo.view_all.assert_called_once()

def test_view_all_empty_list(repo, user_service):
  repo.view_all.return_value = []

  result = user_service.view_all(0, 10)

  assert result == []

  repo.view_all.assert_called_once()

def test_edit_role_success(repo, user_data, user_service):
  repo.check_user_id.return_value = user_data
  repo.save.return_value = user_data

  result = user_service.edit_role(1, UserRole.admin)

  assert result.role == user_data.role

  repo.check_user_id.assert_called_once()
  repo.save.assert_called_once()

def test_edit_role_exception(repo, user_data, user_service):
  repo.check_user_id.return_value = user_data

  with pytest.raises(HTTPException) as exc:
    user_service.edit_role(1, UserRole.user)

  assert exc.value.status_code == 409
  assert exc.value.detail == "User already has this role"

  repo.check_user_id.assert_called_once()

def test_delete_user_success(repo, user_data, user_service):
  repo.check_user_id.return_value = user_data
  repo.delete_user.return_value = {"message": "User deleted"}
  
  result = user_service.delete_user(1)

  assert result == {"message": "User deleted"}

  repo.check_user_id.assert_called_once()
  repo.delete_user.assert_called_once()

def test_delete_user_no_user(repo, user_service):
  repo.check_user_id.return_value = None

  with pytest.raises(HTTPException) as exc:
    user_service.delete_user(1)

  assert exc.value.status_code == 404
  assert exc.value.detail == "User ID not found"

  repo.check_user_id.assert_called_once()