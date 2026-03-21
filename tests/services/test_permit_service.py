import pytest
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError

from tests.fixtures.permit_fixture import secure, config, repo, user_data, created_user, permit_service
from tests.test_database import db_session

from app.models.user_model import UserRole

def test_get_current_user_success(secure, repo, created_user, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {"sub": str(created_user.id), "role": created_user.role}
  repo.check_user_id.return_value = created_user

  result = permit_service.get_current_user(token)

  assert result == created_user

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()

def test_missing_sub(secure, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {}

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 401
  assert exc.value.detail == "Could not validate credentials"

  secure.decode_jwt.assert_called_once()

def test_invalid_token(secure, permit_service):
  token = "invalid token"

  secure.decode_jwt.side_effect = InvalidTokenError

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 401
  assert exc.value.detail == "Could not validate credentials"

  secure.decode_jwt.assert_called_once()

def test_user_not_found(secure, repo, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {"sub": 1, "role": "user"}
  repo.check_user_id.return_value = None

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 401
  assert exc.value.detail == "Could not validate credentials"

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()

def test_get_current_user_inactive(secure, repo, created_user, permit_service):
  token = "valid token"

  user = created_user
  user.is_active = False

  secure.decode_jwt.return_value = {"sub": str(user.id), "role": user.role}
  repo.check_user_id.return_value = user

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 400
  assert exc.value.detail == "User is inactive"

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()

def test_get_current_admin_success(secure, repo, created_user, permit_service):
  token = "valid token"
  created_user.role = UserRole.admin

  secure.decode_jwt.return_value = {"sub": str(created_user.id), "role": created_user.role}
  repo.check_user_id.return_value = created_user

  result = permit_service.get_current_admin(token)

  assert result == created_user

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()

def test_get_suer_token_no_permission(secure, repo, created_user, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {"sub": str(created_user.id), "role": created_user.role}
  repo.check_user_id.return_value = created_user

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_admin(token)

  assert exc.value.status_code == 403
  assert exc.value.detail == "Not enough permission"

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()