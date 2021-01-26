import pytest
from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestDevices:
    @pytest.mark.skip("Skip special case.")
    def test_get_agent_full_disk_access_state(self, connection, device):
        response = connection.devices.get_agent_full_disk_access_state(device["guid"])
        assert_successful_response(response)

    def test_get_by_guid(self, connection, device):
        response = connection.devices.get_by_guid(device["guid"])
        assert_successful_response(response)

    def test_get_settings(self, connection, device):
        response = connection.devices.get_settings(device["guid"])
        assert response.guid == device["guid"]

    def test_deactivate(self, connection, device):
        response = connection.devices.deactivate(device["computerId"])
        assert_successful_response(response)

    @pytest.mark.skip("Skip special case.")
    def test_get_agent_state(self, connection, device):
        response = connection.devices.get_agent_state(device["guid"], "fullDiskAccess")
        assert_successful_response(response)

    def test_get_by_id(self, connection, device):
        response = connection.devices.get_by_id(device["computerId"])
        assert_successful_response(response)

    def test_deauthorize(self, connection, device):
        response = connection.devices.deauthorize(device["computerId"])
        assert_successful_response(response)

    def test_reactivate(self, connection, device):
        response = connection.devices.reactivate(device["computerId"])
        assert_successful_response(response)

    def test_get_all(self, connection, device):
        response_gen = connection.devices.get_all()
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_get_page(self, connection, device):
        response = connection.devices.get_page(1)
        assert_successful_response(response)

    def test_block(self, connection, device):
        response = connection.devices.block(device["computerId"])
        assert_successful_response(response)

    def test_unblock(self, connection, device):
        response = connection.devices.unblock(device["computerId"])
        assert_successful_response(response)
