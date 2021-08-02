
import pytest
from tests.conftest import TEST_SESSION_ID, py42_response

from py42.clients._archiveaccess.restoremanager import FileSizePoller
from py42.clients._archiveaccess.restoremanager import RestoreJobManager
from py42.services.storage.archive import StorageArchiveService
from py42.services.storage.restore import PushRestoreService


@pytest.fixture
def push_service(mocker):
    return mocker.MagicMock(spec=PushRestoreService)


@pytest.fixture
def storage_archive_service(mocker):
    client = mocker.MagicMock(spec=StorageArchiveService)
    response = py42_response(mocker, '{{"webRestoreSessionId": "{0}"}}'.format(TEST_SESSION_ID))
    client.create_restore_session.return_value = response
    return client


@pytest.fixture
def restore_job_manager(mocker):
    return mocker.MagicMock(spec=RestoreJobManager)


@pytest.fixture
def file_size_poller(mocker):
    poller = mocker.MagicMock(spec=FileSizePoller)
    poller.get_file_sizes.return_value = [{u"numFiles": 1, u"numDirs": 1, u"size": 1}]
    return poller


@pytest.fixture
def file_content_chunks():
    return list("file contents")
