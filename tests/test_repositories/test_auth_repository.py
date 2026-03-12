from tests.test_database import db_session
from tests.fixtures.auth_fixture import auth_repo, user_data, created_user

def test_check_username(auth_repo, created_user):
  user = created_user
  found_user = auth_repo.check_username(user.username)

  assert found_user is not None
  assert found_user.username == "user1"