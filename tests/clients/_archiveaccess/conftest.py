import json

import pytest
from tests.clients.conftest import get_file_selection
from tests.conftest import TEST_DOWNLOADS_DIR
from tests.conftest import TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR
from tests.conftest import TEST_SESSION_ID

from py42.clients._archiveaccess import FileType
from py42.clients._archiveaccess.restoremanager import FileSizePoller
from py42.clients._archiveaccess.restoremanager import RestoreJobManager
from py42.response import Py42Response
from py42.services.storage.archive import StorageArchiveService
from py42.services.storage.restore import PushRestoreService


@pytest.fixture
def push_service(mocker):
    return mocker.MagicMock(spec=PushRestoreService)


@pytest.fixture
def storage_archive_service(mocker):
    client = mocker.MagicMock(spec=StorageArchiveService)
    py42_response = mocker.MagicMock(spec=Py42Response)
    py42_response.text = '{{"webRestoreSessionId": "{0}"}}'.format(TEST_SESSION_ID)
    py42_response.status_code = 200
    py42_response.encoding = None
    py42_response.__getitem__ = lambda _, key: json.loads(py42_response.text).get(key)

    client.create_restore_session.return_value = py42_response
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


@pytest.fixture
def single_file_selection():
    return [get_file_selection(FileType.FILE, TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR)]


@pytest.fixture
def double_file_selection():
    return [
        get_file_selection(FileType.FILE, TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR, 1, 2, 3),
        get_file_selection(FileType.DIRECTORY, TEST_DOWNLOADS_DIR, 4, 5, 6),
    ]
