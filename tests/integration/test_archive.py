import os
from datetime import datetime

import pytest
from tests.integration.conftest import assert_successful_response


@pytest.fixture
def device_guid(request):
    return request.config.getini("device_guid")


@pytest.fixture
def destination_device_guid(request):
    return request.config.getini("destination_device_guid")


@pytest.fixture
def archive_guid(request):
    return request.config.getini("archive_guid")


@pytest.fixture
def path(request):
    return request.config.getini("path")


@pytest.fixture
def device(connection, device_guid):
    return connection.devices.get_by_guid(device_guid)


@pytest.mark.integration
class TestArchive:
    def test_get_all_by_device_guid(self, connection, device):
        for response in connection.archive.get_all_by_device_guid(device["computerId"]):
            assert_successful_response(response)
            break

    def test_get_all_device_restore_history(self, connection, device):
        for response in connection.archive.get_all_device_restore_history(
            1, device["computerId"]
        ):
            assert_successful_response(response)
            break

    def test_get_all_org_cold_storage_archives(self, connection, device):
        for response in connection.archive.get_all_org_cold_storage_archives(
            device["orgId"]
        ):
            assert_successful_response(response)
            break

    def test_get_all_org_restore_history(self, connection, device):
        for response in connection.archive.get_all_org_restore_history(
            1, device["orgId"]
        ):
            assert_successful_response(response)
            break

    def test_get_all_user_restore_history(self, connection, device):
        for response in connection.archive.get_all_user_restore_history(
            1, device["userId"]
        ):
            assert_successful_response(response)
            break

    def test_get_backup_sets(self, connection, device_guid, destination_device_guid):
        response = connection.archive.get_backup_sets(
            device_guid, destination_device_guid
        )
        assert_successful_response(response)

    def test_get_by_archive_guid(self, connection, archive_guid):
        response = connection.archive.get_by_archive_guid(archive_guid)
        assert_successful_response(response)

    def test_stream_from_backup(self, connection, device_guid, path):
        response = connection.archive.stream_from_backup(path, device_guid)
        assert_successful_response(response)

    def test_stream_to_destination(self, connection, device_guid, path):
        response = connection.archive.stream_to_destination(
            path, device_guid, device_guid, os.getcwd()
        )
        assert_successful_response(response)

    def test_update_cold_storage_purge_date(self, connection, archive_guid):
        purge_date = datetime.now().strftime("%Y-%m-%d")
        response = connection.archive.update_cold_storage_purge_date(
            archive_guid, purge_date
        )
        assert_successful_response(response)
