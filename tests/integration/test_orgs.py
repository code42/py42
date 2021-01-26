import pytest

from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestOrg:
    def test_get_agent_full_disk_access_states(self, connection, org):
        response = connection.orgs.get_agent_full_disk_access_states(org["orgId"])
        assert_successful_response(response)

    def test_get_by_id(self, connection, org):
        response = connection.orgs.get_by_id(org["orgId"])
        assert_successful_response(response)

    def test_get_page(self, connection):
        response = connection.orgs.get_page(1)
        assert_successful_response(response)

    def test_get_agent_state(self, connection, org):
        response = connection.orgs.get_agent_state(org["orgId"], "fullDiskAccess")
        assert_successful_response(response)

    def test_get_by_uid(self, connection, org):
        response = connection.orgs.get_by_uid(org["orgUid"])
        assert_successful_response(response)

    @pytest.mark.skip("Fails when whole test suite is executed.")
    def test_deactivate(self, connection, org):
        response = connection.orgs.deactivate(org["orgId"])
        assert_successful_response(response)

    def test_reactivate(self, connection, org):
        response = connection.orgs.reactivate(org["orgId"])
        assert_successful_response(response)

    def test_get_all(self, connection):
        response_gen = connection.orgs.get_all()
        for response in response_gen:
            assert_successful_response(response)

    def test_get_current(self, connection):
        response = connection.orgs.get_current()
        assert_successful_response(response)

    def test_block(self, connection, org):
        response = connection.orgs.block(org["orgId"])
        assert_successful_response(response)

    def test_unblock(self, connection, org):
        response = connection.orgs.unblock(org["orgId"])
        assert_successful_response(response)
