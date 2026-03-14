import pytest
from fastapi import HTTPException

from tests.fixtures.auth_fixture import secure, config, repo, auth_service, user_data

def test_login_success(secure, repo, auth_service, user_data):
  user_data.id = 1

  repo.check_username.return_value = user_data
  secure.verify_password.return_value = True
  secure.encode_jwt.return_value = "jwt_token"

  token = auth_service.login("user1", "Password123")

  assert token.access_token == "jwt_token"
  assert token.token_type == "bearer"

  repo.check_username.assert_called_once()
  secure.verify_password.assert_called_once()
  secure.encode_jwt.assert_called_once()

def test_login_username_failure(secure, repo, auth_service):
  repo.check_username.return_value = None
  secure.verify_password.return_value = False

  with pytest.raises(HTTPException) as exc:
    auth_service.login("user1", "Password123")

  assert exc.value.status_code == 401
  assert "Incorrect" in str(exc.value)

  repo.check_username.assert_called_once()
  secure.verify_password.assert_called_once()

def test_login_password_failure(secure, repo, auth_service, user_data):
  repo.check_username.return_value = user_data
  secure.verify_password.return_value = False

  with pytest.raises(HTTPException) as exc:
    auth_service.login("user1", "Wrongpassword123")

  assert exc.value.status_code == 401
  assert "Incorrect" in str(exc.value)

  repo.check_username.assert_called_once()
  secure.verify_password.assert_called_once()