from tests.test_database import db_session
from tests.fixtures.permit_fixture import permit_repo, user_data, created_user

def test_check_user_id(permit_repo, created_user):
  found_id = permit_repo.check_user_id(created_user.id)

  assert found_id.id == created_user.id