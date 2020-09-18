# -*- coding: utf-8 -*-
import json
import pytest
from py42.clients._archiveaccess import FileType, FileSelection

from py42.response import Py42Response
from py42.services.storage.archive import StorageArchiveService
from py42.clients._archiveaccess.restoremanager import RestoreJobManager
from py42.clients._archiveaccess.restoremanager import FileSizePoller


DEVICE_GUID = "device-guid"
DESTINATION_GUID = "destination-guid"
WEB_RESTORE_SESSION_ID = "FAKE_SESSION_ID"
FILE_ID = "file-id"
DESKTOP_ID = "97c6bd9bff714bd45665130f7f381781"
DOWNLOADS_ID = "69e930e774cbc1ee6d0c0ff2ba5804ee"
PATH_TO_FILE_IN_DOWNLOADS_FOLDER = "/Users/qa/Downloads/terminator-genisys.jpg"
PATH_TO_DESKTOP_FOLDER = "/Users/qa/Desktop"


@pytest.fixture
def storage_archive_service(mocker):
    client = mocker.MagicMock(spec=StorageArchiveService)
    py42_response = mocker.MagicMock(spec=Py42Response)
    py42_response.text = '{{"webRestoreSessionId": "{0}"}}'.format(
        WEB_RESTORE_SESSION_ID
    )
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
    return [get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER)]


@pytest.fixture
def double_file_selection():
    return [
        get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER, 1, 2, 3),
        get_file_selection(FileType.DIRECTORY, PATH_TO_DESKTOP_FOLDER, 4, 5, 6),
    ]


def get_file_selection(file_type, file_path, num_files=1, num_dirs=1, num_bytes=1):
    return FileSelection(
        {"fileType": file_type, "path": file_path, "selected": True},
        num_files,
        num_dirs,
        num_bytes,
    )
