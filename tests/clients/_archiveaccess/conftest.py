import pytest
from tests.conftest import create_mock_response
from tests.conftest import TEST_SESSION_ID

from pycpg.clients._archiveaccess.restoremanager import FileSizePoller
from pycpg.clients._archiveaccess.restoremanager import RestoreJobManager
from pycpg.services.storage.archive import StorageArchiveService
from pycpg.services.storage.restore import PushRestoreService


@pytest.fixture
def push_service(mocker):
    return mocker.MagicMock(spec=PushRestoreService)


@pytest.fixture
def storage_archive_service(mocker):
    client = mocker.MagicMock(spec=StorageArchiveService)
    response = create_mock_response(
        mocker, f'{{"webRestoreSessionId": "{TEST_SESSION_ID}"}}'
    )
    client.create_restore_session.return_value = response
    return client


@pytest.fixture
def restore_job_manager(mocker):
    return mocker.MagicMock(spec=RestoreJobManager)


@pytest.fixture
def file_size_poller(mocker):
    poller = mocker.MagicMock(spec=FileSizePoller)
    poller.get_file_sizes.return_value = [{"numFiles": 1, "numDirs": 1, "size": 1}]
    return poller


@pytest.fixture
def file_content_chunks():
    return list("file contents")
