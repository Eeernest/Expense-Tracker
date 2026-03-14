from tests.test_database import db_session
from tests.fixtures.permit_fixture import permit_repo, user_data, created_user

def test_check_user_id(permit_repo, created_user):
  user = created_user
  found_id = permit_repo.check_user_id(user.id)

  assert found_id is not None
  assert found_id.id == 1