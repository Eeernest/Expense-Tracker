from tests.test_database import db_session
from tests.fixtures.auth_fixture import auth_repo, user_data, created_user

def test_check_username(auth_repo, created_user):
  result = auth_repo.check_username(created_user.username)

  assert result is not None
  assert result.username == "user1"