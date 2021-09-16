import pytest
from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestTrustedActivities:
    @pytest.fixture(scope="module")
    # def trusted_activity(self, connection):
    #     return connection.trustedactivities.create("DOMAIN", 'test.com')
    #
    # def test_get_all_trusted_activities(
    #     self, connection,
    # ):
    #     page_gen = connection.trustedactivites.get_all()
    #     for response in page_gen:
    #         assert_successful_response(response)
    #         break
    def test_get_trusted_activity(self, connection, trusted_activity):
        response = connection.cases.get(trusted_activity["resourceId"])
        assert_successful_response(response)

    # def test_update_trusted_activity(self, connection, trusted_activity):
    #     response = connection.trustedactivities.update(trusted_activity["resourceId"], description="integration test case")
    #     assert_successful_response(response)
    #
    # def test_delete_trusted_activity(self, connection, trusted_activity):
    #     response = connection.trustedactivities.delete(trusted_activity["resourceId"])
    #     assert_successful_response(response)
