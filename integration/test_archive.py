from datetime import datetime

import pytest

from py42.exceptions import Py42ForbiddenError

device_guid = "935873453596901068"
device_id = "110395"
org_id = "2689"
user_id = "176457"
destination_device_guid = "673679195225718785"
archive_guid = "912100293346985227"
path = "C:/Users/QA/Downloads/spatel_add.csv"
purge_date = datetime.now().strftime("%Y-%m-%d")


def test_get_all_by_device_guid(connection):
    for response in connection.archive.get_all_by_device_guid(device_guid):
        assert response.status_code == 200
        break


def test_get_all_device_restore_history(connection):
    for response in connection.archive.get_all_device_restore_history(1, device_id):
        assert response.status_code == 200
        break


def test_get_all_org_cold_storage_archives(connection):
    for response in connection.archive.get_all_org_cold_storage_archives(org_id):
        assert response.status_code == 200
        break


def test_get_all_org_restore_history(connection):
    for response in connection.archive.get_all_org_restore_history(1, org_id):
        assert response.status_code == 200
        break


def test_get_all_user_restore_history(connection):
    for response in connection.archive.get_all_user_restore_history(1, user_id):
        assert response.status_code == 200
        break


def test_get_backup_sets(connection):
    response = connection.archive.get_backup_sets(device_guid, destination_device_guid)
    assert response.status_code == 200


def test_get_by_archive_guid(connection):
    response = connection.archive.get_by_archive_guid(archive_guid)
    assert response.status_code == 200


def test_stream_from_backup(connection):
    response = connection.archive.stream_from_backup(path, device_guid)
    assert response.status_code == 200


def test_update_cold_storage_purge_date(connection):
    with pytest.raises(Py42ForbiddenError):
        connection.archive.update_cold_storage_purge_date(archive_guid, purge_date)
