from tests.test_database import db_session
from tests.fixtures.auth_fixture import fx_repo, user_data

def test_check_username(fx_repo, user_data):
  fx_repo.create_repo(user_data)

  found_user = fx_repo.check_username(user_data.username)

  assert found_user is not None
  assert found_user.username == "user1"