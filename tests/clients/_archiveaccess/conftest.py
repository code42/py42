# -*- coding: utf-8 -*-
import json
from requests import Response

from py42.response import Py42Response
from py42.services.archive import ArchiveService
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.storage.archive import StorageArchiveService
from py42.clients._archiveaccess.restoremanager import RestoreJobManager
from py42.clients._archiveaccess._accessor_factory import ArchiveAccessorFactory
from py42.clients._archiveaccess import FileSelection
from py42.clients._archiveaccess.restoremanager import FileSizePoller


DEVICE_GUID = "device-guid"
INVALID_DEVICE_GUID = "invalid-device-guid"
DESTINATION_GUID = "destination-guid"
DATA_KEY_TOKEN = "FAKE_DATA_KEY_TOKEN"
WEB_RESTORE_SESSION_ID = "FAKE_SESSION_ID"
FILE_ID = "file-id"

USERS_DIR = "/Users"
PATH_TO_FILE_IN_DOWNLOADS_FOLDER = "/Users/qa/Downloads/terminator-genisys.jpg"
PATH_TO_DESKTOP_FOLDER = "/Users/qa/Desktop"
PATH_TO_DOWNLOADS_FOLDER = "/Users/qa/Downloads"

DESKTOP_ID = "97c6bd9bff714bd45665130f7f381781"
DOWNLOADS_ID = "69e930e774cbc1ee6d0c0ff2ba5804ee"


class GetFilePathMetadataResponses(object):
    @staticmethod
    def get_file_id_from_request(response):
        return response[1]

    WINDOWS_NULL_ID = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:08:37.000-05:00",
                    "filename": "/",
                    "lastBackup": "2019-04-12T12:56:55.023-05:00",
                    "lastBackupMs": 1555091815023,
                    "date": "04/12/19 12:56 PM",
                    "path": "C:/",
                    "hidden": false,
                    "lastModifiedMs": 1529680117000,
                    "type": "directory",
                    "id": null
                }
            ]
        """,
        None,
    )

    NULL_ID = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:08:37.000-05:00",
                    "filename": "/",
                    "lastBackup": "2019-04-12T12:56:55.023-05:00",
                    "lastBackupMs": 1555091815023,
                    "date": "04/12/19 12:56 PM",
                    "path": "/",
                    "hidden": false,
                    "lastModifiedMs": 1529680117000,
                    "type": "directory",
                    "id": "885bf69dc0168f3624435346d7bf4836"
                }
            ]
        """,
        None,
    )

    ROOT = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:02:44.000-05:00",
                    "filename": "Users",
                    "lastBackup": "2019-04-12T12:56:55.090-05:00",
                    "lastBackupMs": 1555091815090,
                    "date": "04/12/19 12:56 PM",
                    "path": "/Users",
                    "hidden": false,
                    "lastModifiedMs": 1529679764000,
                    "type": "directory",
                    "id": "c2dc0a9bc27be41cb84d6ae91f6a0974"
                }
            ]
        """,
        "885bf69dc0168f3624435346d7bf4836",
    )

    USERS = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-19T14:58:36.000-05:00",
                    "filename": "qa",
                    "lastBackup": "2019-04-12T12:56:55.095-05:00",
                    "lastBackupMs": 1555091815095,
                    "date": "04/12/19 12:56 PM",
                    "path": "/Users/qa",
                    "hidden": false,
                    "lastModifiedMs": 1529438316000,
                    "type": "directory",
                    "id": "8f939e90bae37f9ec860ced08c5ffb7f"
                }
            ]
        """,
        "c2dc0a9bc27be41cb84d6ae91f6a0974",
    )

    USERS_QA = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-19T14:54:46.000-05:00",
                    "filename": ".bash_history",
                    "lastBackup": "2019-04-12T13:01:00.832-05:00",
                    "lastBackupMs": 1555092060832,
                    "date": "04/12/19 01:01 PM",
                    "path": "/Users/qa/.bash_history",
                    "hidden": true,
                    "lastModifiedMs": 1529438086000,
                    "type": "file",
                    "id": "97d8328d121983727cf854dc861d1ada"
                },
                {
                    "deleted": false,
                    "lastModified": "2018-06-19T14:58:36.000-05:00",
                    "filename": "Applications",
                    "lastBackup": "2019-04-12T13:00:35.478-05:00",
                    "lastBackupMs": 1555092035478,
                    "date": "04/12/19 01:00 PM",
                    "path": "/Users/qa/Applications",
                    "hidden": false,
                    "lastModifiedMs": 1529438316000,
                    "type": "directory",
                    "id": "13cc0e21c1f14ff102206edd44bfc6bc"
                },
                {
                    "deleted": false,
                    "lastModified": "2019-04-18T12:56:34.000-05:00",
                    "filename": "Desktop",
                    "lastBackup": "2019-04-19T03:01:11.566-05:00",
                    "lastBackupMs": 1555660871566,
                    "date": "04/19/19 03:01 AM",
                    "path": "/Users/qa/Desktop",
                    "hidden": false,
                    "lastModifiedMs": 1555610194000,
                    "type": "directory",
                    "id": "97c6bd9bff714bd45665130f7f381781"
                },
                {
                    "deleted": false,
                    "lastModified": "2018-02-12T12:30:03.000-06:00",
                    "filename": "Documents",
                    "lastBackup": "2019-04-12T13:04:18.169-05:00",
                    "lastBackupMs": 1555092258169,
                    "date": "04/12/19 01:04 PM",
                    "path": "/Users/qa/Documents",
                    "hidden": false,
                    "lastModifiedMs": 1518460203000,
                    "type": "directory",
                    "id": "9db2b57abab79c4a92c939ec82d3dd0e"
                },
                {
                    "deleted": false,
                    "lastModified": "2019-04-12T12:58:34.000-05:00",
                    "filename": "Downloads",
                    "lastBackup": "2019-04-12T13:01:00.891-05:00",
                    "lastBackupMs": 1555092060891,
                    "date": "04/12/19 01:01 PM",
                    "path": "/Users/qa/Downloads",
                    "hidden": false,
                    "lastModifiedMs": 1555091914000,
                    "type": "directory",
                    "id": "f939cfc4d476ec5535ccb0f6c0377ef4"
                },
                {
                    "deleted": false,
                    "lastModified": "2019-04-12T10:43:49.000-05:00",
                    "filename": "Library",
                    "lastBackup": "2019-04-12T12:59:49.676-05:00",
                    "lastBackupMs": 1555091989676,
                    "date": "04/12/19 12:59 PM",
                    "path": "/Users/qa/Library",
                    "hidden": false,
                    "lastModifiedMs": 1555083829000,
                    "type": "directory",
                    "id": "bcf31dab21a4f7d4f67b812d6c891ed9"
                }
            ]
        """,
        "8f939e90bae37f9ec860ced08c5ffb7f",
    )

    USERS_QA_DOWNLOADS = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2019-04-12T12:58:13.000-05:00",
                    "filename": "Terminator II Screenplay.pdf",
                    "lastBackup": "2019-04-12T13:05:10.089-05:00",
                    "lastBackupMs": 1555092310089,
                    "date": "04/12/19 01:05 PM",
                    "path": "/Users/qa/Downloads/Terminator II Screenplay.pdf",
                    "hidden": false,
                    "lastModifiedMs": 1555091893000,
                    "type": "file",
                    "id": "f63aeee85943809ead0cb11cdc773625"
                },
                {
                    "deleted": true,
                    "lastModified": "2019-04-12T12:57:43.000-05:00",
                    "filename": "terminator-genisys.jpg",
                    "lastBackup": "2019-04-12T13:05:10.087-05:00",
                    "lastBackupMs": 1555092310087,
                    "date": "04/12/19 01:05 PM",
                    "path": "/Users/qa/Downloads/terminator-genisys.jpg",
                    "hidden": false,
                    "lastModifiedMs": 1555091863000,
                    "type": "file",
                    "id": "69e930e774cbc1ee6d0c0ff2ba5804ee"
                }
            ]
        """,
        "f939cfc4d476ec5535ccb0f6c0377ef4",
    )

    WINDOWS = (
        """[
                {
                    "deleted": true,
                    "lastModified": "2019-04-12T12:57:43.000-05:00",
                    "filename": "terminator-genisys.jpg",
                    "lastBackup": "2019-04-12T13:05:10.087-05:00",
                    "lastBackupMs": 1555092310087,
                    "date": "04/12/19 01:05 PM",
                    "path": "C:/Users/The Terminator/Documents/file.txt",
                    "hidden": false,
                    "lastModifiedMs": 1555091863000,
                    "type": "file",
                    "id": "1234cfc4d467895535abcdf6c00000f4"
                }
            ]
        """,
        "1234cfc4d467895535abcdf6c00000f4",
    )


class GetWebRestoreJobResponses(object):

    MISSING_STATUS = """{
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": true,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979,
                "percentComplete": 0
            }
        """

    NOT_DONE = """{
                "status": "preparing",
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": false,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979,
                "percentComplete": 0
            }
        """

    DONE = """{
                "status": "done",
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": true,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979
            }
        """


@pytest.fixture
def archive_client(mocker):
    client = mocker.MagicMock(spec=ArchiveService)
    py42_response = mocker.MagicMock(spec=Py42Response)
    py42_response.text = '{{"dataKeyToken": "{0}"}}'.format(DATA_KEY_TOKEN)
    py42_response.status_code = 200
    py42_response.encoding = None
    py42_response.__getitem__ = lambda _, key: json.loads(py42_response.text).get(key)
    client.get_data_key_token.return_value = py42_response
    return client


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
def storage_service_factory(mocker, storage_archive_service):
    factory = mocker.MagicMock(spec=StorageServiceFactory)
    factory.create_archive_service.return_value = storage_archive_service
    return factory


@pytest.fixture
def restore_job_manager(mocker):
    return mocker.MagicMock(spec=RestoreJobManager)


@pytest.fixture
def file_size_poller(mocker):
    poller = mocker.MagicMock(spec=FileSizePoller)
    poller.get_file_sizes.return_value = [{u"numFiles": 1, u"numDirs": 1, u"size": 1}]
    return poller


@pytest.fixture
def single_file_selection():
    return [get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER)]


@pytest.fixture
def double_file_selection():
    return [
        get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER, 1, 2, 3),
        get_file_selection(FileType.DIRECTORY, PATH_TO_DESKTOP_FOLDER, 4, 5, 6),
    ]


@pytest.fixture
def single_dir_selection():
    return [get_file_selection(FileType.DIRECTORY, PATH_TO_DOWNLOADS_FOLDER)]


@pytest.fixture
def file_content_chunks():
    return list("file contents")


def mock_start_restore_response(mocker, storage_archive_service, response):
    def mock_start_restore(
        device_guid,
        web_restore_session_id,
        restore_groups,
        num_files,
        num_dirs,
        num_bytes,
        **kwargs
    ):
        start_restore_response = mocker.MagicMock(spec=Response)
        start_restore_response.text = response
        start_restore_response.status_code = 200
        return Py42Response(start_restore_response)

    storage_archive_service.start_restore.side_effect = mock_start_restore


def mock_get_restore_status_responses(mocker, storage_archive_service, json_responses):
    responses = []
    for json_response in json_responses:
        get_restore_status_response = mocker.MagicMock(spec=Response)
        get_restore_status_response.text = json_response
        get_restore_status_response.status_code = 200
        responses.append(Py42Response(get_restore_status_response))

    storage_archive_service.get_restore_status.side_effect = responses


def stream_restore_result_response_mock(mocker, storage_archive_service, chunks):
    stream_restore_result_response = mocker.MagicMock(spec=Py42Response)

    def mock_stream_restore_result(job_id, **kwargs):
        stream_restore_result_response.iter_content.return_value = chunks
        return stream_restore_result_response

    storage_archive_service.stream_restore_result.side_effect = (
        mock_stream_restore_result
    )

    return stream_restore_result_response


def get_get_file_path_metadata_mock(mocker, session_id, device_guid, responses):
    """Mock responses to StorageArchiveService.get_file_path_metadata(). Responses are returned in the same order as
    they are in the given `responses` list"""

    file_id_responses = {}
    for response in responses:
        file_id = GetFilePathMetadataResponses.get_file_id_from_request(response)
        if file_id:
            file_id_responses[file_id] = response[0]
        else:
            if None in file_id_responses:
                raise Exception(
                    "Response list already has a response for a 'None' fileId"
                )
            file_id_responses[None] = response[0]

    def mock_get_file_path_metadata(*args, **kwargs):
        if not args[0] == session_id:
            raise Exception("Unexpected archive connection ID")

        if not args[1] == device_guid:
            raise Exception("Unexpected device GUID")

        file_id = kwargs["file_id"]

        if file_id not in file_id_responses:
            raise Exception("Unexpected request with file_id: {}".format(file_id))

        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.text = file_id_responses[file_id]
        get_file_path_metadata_response = Py42Response(mock_response)

        return get_file_path_metadata_response

    return mock_get_file_path_metadata


def get_file_selection(file_type, file_path, num_files=1, num_dirs=1, num_bytes=1):
    return FileSelection(
        {"fileType": file_type, "path": file_path, "selected": True},
        num_files,
        num_dirs,
        num_bytes,
    )


def mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses):
    # responses = [item[0] for item in responses]
    storage_archive_service.get_file_path_metadata.side_effect = get_get_file_path_metadata_mock(
        mocker, WEB_RESTORE_SESSION_ID, DEVICE_GUID, responses
    )


def mock_walking_to_downloads_folder(mocker, storage_archive_service):
    responses = [
        GetFilePathMetadataResponses.NULL_ID,
        GetFilePathMetadataResponses.ROOT,
        GetFilePathMetadataResponses.USERS,
        GetFilePathMetadataResponses.USERS_QA,
        GetFilePathMetadataResponses.USERS_QA_DOWNLOADS,
    ]
    mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses)


def mock_walking_tree_for_windows_path(mocker, storage_archive_service):
    responses = [GetFilePathMetadataResponses.WINDOWS_NULL_ID]
    mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses)


def get_response_job_id(response_str):
    return json.loads(response_str)["jobId"]
