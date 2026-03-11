from app.services.user_service import UserService
from app.models.user_model import UserRole
from app.schemas.user_schema import UserCreate

from tests.fixtures.user_fixture import create_data, secure, config, repo, user_service

import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from pydantic import ValidationError

def test_create_account_success(create_data, secure, repo, user_service):
  repo.check_username.return_value = None
  repo.check_email.return_value = None

  secure.get_password_hash.return_value = "Hashedpassword123"

  repo.create_repo.return_value = Mock(
    username="user1",
    email="user1@example.com",
    role=UserRole.user
  )

  created_user = user_service.create_account(create_data)

  assert created_user.username == "user1"
  assert created_user.role == UserRole.user

  secure.get_password_hash.assert_called_once()
  repo.create_repo.assert_called_once()

def test_username_failure(create_data, secure, repo, user_service):
  repo.check_username.return_value = Mock()

  with pytest.raises(HTTPException) as exc:
    user_service.create_account(create_data)

  assert exc.value.status_code == 409
  repo.create_repo.assert_not_called()

def test_email_failure(create_data, secure, repo, user_service):
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