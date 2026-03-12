import pytest
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError

from tests.fixtures.permit_fixture import secure, config, repo, user_data, created_user, permit_service
from tests.test_database import db_session

def test_get_current_user_success(secure, repo, created_user, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {"sub": str(created_user.id)}
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
  assert "Could" in str(exc.value)

  secure.decode_jwt.assert_called_once()

def test_invalid_token(secure, permit_service):
  token = "invalid token"

  secure.decode_jwt.side_effect = InvalidTokenError

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 401
  assert "Could" in str(exc.value)

  secure.decode_jwt.assert_called_once()

def test_user_not_found(secure, repo, permit_service):
  token = "valid token"

  secure.decode_jwt.return_value = {"sub": 1}
  repo.check_user_id.return_value = None

  with pytest.raises(HTTPException) as exc:
    permit_service.get_current_user(token)

  assert exc.value.status_code == 401
  assert "Could" in str(exc.value)

  secure.decode_jwt.assert_called_once()
  repo.check_user_id.assert_called_once()