# -*- coding: utf-8 -*-
import json

import pytest
from requests import Response

import py42.util
from py42._internal.archive_access import ArchiveAccessor
from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.archive_access import FileSelection
from py42._internal.archive_access import FileSizePoller
from py42._internal.archive_access import FileType
from py42._internal.archive_access import RestoreJobManager
from py42._internal.clients.archive import ArchiveClient
from py42._internal.clients.storage import StorageArchiveClient
from py42._internal.clients.storage import StorageClient
from py42._internal.clients.storage import StorageClientFactory
from py42.exceptions import Py42ArchiveFileNotFoundError
from py42.response import Py42Response

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
                "status": "preparing",
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


@pytest.fixture
def archive_client(mocker):
    client = mocker.MagicMock(spec=ArchiveClient)
    py42_response = mocker.MagicMock(spec=Py42Response)
    py42_response.text = '{{"dataKeyToken": "{0}"}}'.format(DATA_KEY_TOKEN)
    py42_response.status_code = 200
    py42_response.encoding = None
    py42_response.__getitem__ = lambda _, key: json.loads(py42_response.text).get(key)
    client.get_data_key_token.return_value = py42_response
    return client


@pytest.fixture
def storage_archive_client(mocker):
    client = mocker.MagicMock(spec=StorageArchiveClient)
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
def storage_client(mocker):
    return mocker.MagicMock(spec=StorageClient)


@pytest.fixture
def storage_client_factory(mocker, storage_client, storage_archive_client):
    factory = mocker.MagicMock(spec=StorageClientFactory)
    factory.from_device_guid.return_value = storage_archive_client
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


def mock_start_restore_response(mocker, storage_archive_client, response):
    def mock_start_restore(
        guid,
        web_restore_session_id,
        path_set,
        num_files,
        num_dirs,
        size,
        zip_result,
        **kwargs
    ):
        start_restore_response = mocker.MagicMock(spec=Response)
        start_restore_response.text = response
        start_restore_response.status_code = 200
        return Py42Response(start_restore_response)

    storage_archive_client.start_restore.side_effect = mock_start_restore


def mock_get_restore_status_responses(mocker, storage_archive_client, json_responses):
    responses = []
    for json_response in json_responses:
        get_restore_status_response = mocker.MagicMock(spec=Response)
        get_restore_status_response.text = json_response
        get_restore_status_response.status_code = 200
        responses.append(Py42Response(get_restore_status_response))

    storage_archive_client.get_restore_status.side_effect = responses


def stream_restore_result_response_mock(mocker, storage_archive_client, chunks):
    stream_restore_result_response = mocker.MagicMock(spec=Py42Response)

    def mock_stream_restore_result(job_id, **kwargs):
        stream_restore_result_response.iter_content.return_value = chunks
        return stream_restore_result_response

    storage_archive_client.stream_restore_result.side_effect = (
        mock_stream_restore_result
    )

    return stream_restore_result_response


def get_get_file_path_metadata_mock(mocker, session_id, device_guid, responses):
    """Mock responses to StorageArchiveClient.get_file_path_metadata(). Responses are returned in the same order as
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
            raise Exception("Unexpected archive session ID")

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


def get_file_selection(file_type, file_path, num_files=1, num_dirs=1, size=1):
    return FileSelection(
        {"type": file_type, "path": file_path, "selected": True},
        num_files,
        num_dirs,
        size,
    )


def mock_get_file_path_metadata_responses(mocker, storage_archive_client, responses):
    # responses = [item[0] for item in responses]
    storage_archive_client.get_file_path_metadata.side_effect = get_get_file_path_metadata_mock(
        mocker, WEB_RESTORE_SESSION_ID, DEVICE_GUID, responses
    )


def mock_walking_to_downloads_folder(mocker, storage_archive_client):
    responses = [
        GetFilePathMetadataResponses.NULL_ID,
        GetFilePathMetadataResponses.ROOT,
        GetFilePathMetadataResponses.USERS,
        GetFilePathMetadataResponses.USERS_QA,
        GetFilePathMetadataResponses.USERS_QA_DOWNLOADS,
    ]
    mock_get_file_path_metadata_responses(mocker, storage_archive_client, responses)


def mock_walking_tree_for_windows_path(mocker, storage_archive_client):
    responses = [GetFilePathMetadataResponses.WINDOWS_NULL_ID]
    mock_get_file_path_metadata_responses(mocker, storage_archive_client, responses)


def get_response_job_id(response_str):
    return json.loads(response_str)["jobId"]


class TestArchiveAccessManager(object):
    def test_archive_accessor_manager_constructor_constructs_successfully(
        self, archive_client, storage_client_factory
    ):
        assert ArchiveAccessorManager(archive_client, storage_client_factory)

    def test_get_archive_accessor_with_device_guid_and_destination_guid_returns(
        self,
        archive_client,
        storage_client_factory,
        storage_client,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )

        assert accessor_manager.get_archive_accessor(DEVICE_GUID, DESTINATION_GUID)

    def test_get_archive_accessor_calls_storage_client_factory_with_correct_args(
        self,
        archive_client,
        storage_client_factory,
        storage_client,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(DEVICE_GUID)
        storage_client_factory.from_device_guid.assert_called_with(
            DEVICE_GUID, destination_guid=None
        )

    def test_get_archive_accessor_with_opt_dest_guid_calls_storage_client_factory_with_correct_args(
        self,
        archive_client,
        storage_client_factory,
        storage_client,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(
            DEVICE_GUID, destination_guid=DESTINATION_GUID
        )
        storage_client_factory.from_device_guid.assert_called_with(
            DEVICE_GUID, destination_guid=DESTINATION_GUID
        )

    def test_get_archive_accessor_creates_web_restore_session_with_correct_args(
        self,
        archive_client,
        storage_client,
        storage_client_factory,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(DEVICE_GUID)

        storage_archive_client.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN
        )

    def test_get_archive_accessor_when_given_private_password_creates_expected_restore_session(
        self,
        archive_client,
        storage_client,
        storage_client_factory,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(
            DEVICE_GUID, private_password="TEST_PASSWORD"
        )

        storage_archive_client.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN, private_password="TEST_PASSWORD"
        )

    def test_get_archive_accessor_when_given_encryption_key_creates_expected_restore_session(
        self,
        archive_client,
        storage_client,
        storage_client_factory,
        storage_archive_client,
    ):
        storage_client.archive = storage_archive_client
        storage_client_factory.from_device_guid.return_value = storage_client
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(DEVICE_GUID, encryption_key="TEST_KEY")

        storage_archive_client.create_restore_session.assert_called_once_with(
            DEVICE_GUID, encryption_key="TEST_KEY"
        )

    def test_get_archive_accessor_calls_create_restore_job_manager_with_correct_args(
        self,
        mocker,
        archive_client,
        storage_client_factory,
        storage_archive_client,
        storage_client,
    ):
        spy = mocker.spy(py42._internal.archive_access, "create_restore_job_manager")
        storage_client.archive = storage_archive_client

        storage_client_factory.from_device_guid.return_value = storage_client

        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        accessor_manager.get_archive_accessor(DEVICE_GUID)

        assert spy.call_count == 1
        spy.assert_called_once_with(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

    def test_get_archive_accessor_raises_exception_when_create_backup_client_raises(
        self, archive_client, storage_client_factory
    ):
        storage_client_factory.from_device_guid.side_effect = Exception(
            "Exception in create_backup_client"
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_client_factory
        )
        with pytest.raises(Exception):
            accessor_manager.get_archive_accessor(INVALID_DEVICE_GUID)


class TestArchiveAccessor(object):
    def test_archive_accessor_constructor_constructs_successfully(
        self, storage_archive_client, restore_job_manager, file_size_poller
    ):
        assert ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )

    def test_stream_from_backup_with_root_folder_path_calls_get_stream(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller
    ):
        mock_get_file_path_metadata_responses(
            mocker, storage_archive_client, [GetFilePathMetadataResponses.NULL_ID]
        )
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup("/", file_size_calc_timeout=0)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "/")]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_root_level_folder_calls_get_stream(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller
    ):
        mock_get_file_path_metadata_responses(
            mocker,
            storage_archive_client,
            [GetFilePathMetadataResponses.NULL_ID, GetFilePathMetadataResponses.ROOT],
        )
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(USERS_DIR)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, USERS_DIR)]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_file_path_calls_get_stream(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            PATH_TO_FILE_IN_DOWNLOADS_FOLDER, file_size_calc_timeout=0
        )
        expected_file_selection = [
            get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER)
        ]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_normalizes_windows_paths(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_tree_for_windows_path(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup("C:\\", file_size_calc_timeout=0)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "C:/")]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_calls_get_file_size_with_expected_params(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            PATH_TO_FILE_IN_DOWNLOADS_FOLDER, file_size_calc_timeout=10
        )
        file_size_poller.get_file_sizes.assert_called_once_with(
            [DOWNLOADS_ID], timeout=10
        )

    def test_stream_from_backup_when_not_ignoring_file_size_calc_returns_size_sums_from_response(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )

        def get_file_sizes(*args, **kwargs):
            return [
                {"numFiles": 1, "numDirs": 2, "size": 3},
                {"numFiles": 4, "numDirs": 5, "size": 6},
            ]

        file_size_poller.get_file_sizes.side_effect = get_file_sizes
        archive_accessor.stream_from_backup(
            [PATH_TO_FILE_IN_DOWNLOADS_FOLDER, PATH_TO_DESKTOP_FOLDER],
        )
        expected_file_selection = [
            get_file_selection(
                FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER, 1, 2, 3,
            ),
            get_file_selection(FileType.DIRECTORY, PATH_TO_DESKTOP_FOLDER, 4, 5, 6,),
        ]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_file_not_in_archive_raises_exception(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = "/Users/qa/Downloads/file-not-in-archive.txt"
        with pytest.raises(Exception) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)
        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_unicode_file_path_not_in_archive_raises_exception(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = u"/Users/qa/Downloads/吞"

        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)
        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_drive_not_in_archive_raises_exception(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "C:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)

        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_case_sensitive_drive_not_in_archive_raises_exception(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "c:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)

        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_uses_show_deleted_param_on_get_file_path_metadata(
        self, mocker, storage_archive_client, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_client)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_client,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(PATH_TO_FILE_IN_DOWNLOADS_FOLDER)
        storage_archive_client.get_file_path_metadata.assert_called_with(
            WEB_RESTORE_SESSION_ID, DEVICE_GUID, file_id=mocker.ANY, show_deleted=True
        )


class TestFileSizePoller(object):
    def test_get_file_sizes_returns_sizes_for_each_id(
        self, mocker, storage_archive_client
    ):

        DESKTOP_SIZE_JOB = "DESKTOP_SIZE_JOB"
        DOWNLOADS_SIZE_JOB = "DOWNLOAD_SIZE_JOB"

        def create_job(guid, file_id, timestamp, show_deleted):
            resp = mocker.MagicMock(spec=Response)
            if file_id == DESKTOP_ID:
                resp.text = json.dumps({"jobId": DESKTOP_SIZE_JOB})
            elif file_id == DOWNLOADS_ID:
                resp.text = json.dumps({"jobId": DOWNLOADS_SIZE_JOB})

            return Py42Response(resp)

        DESKTOP_SIZES = {"numDirs": 1, "numFiles": 2, "size": 3}
        DOWNLOADS_SIZES = {"numDirs": 4, "numFiles": 5, "size": 6}

        def get_sizes(job_id, device_id):
            resp = mocker.MagicMock(spec=Response)
            if job_id == DESKTOP_SIZE_JOB:
                resp.text = json.dumps(DESKTOP_SIZES)
            elif job_id == DOWNLOADS_SIZE_JOB:
                resp.text = json.dumps(DOWNLOADS_SIZES)
            return Py42Response(resp)

        def get_status(job_id, device_guid):
            resp = mocker.MagicMock(spec=Response)
            base_obj = {"status": "DONE"}
            if job_id == DESKTOP_SIZE_JOB:
                DESKTOP_SIZES["status"] = "DONE"
                resp.text = json.dumps(DESKTOP_SIZES)
            elif job_id == DOWNLOADS_SIZE_JOB:
                DOWNLOADS_SIZES["status"] = "DONE"
                resp.text = json.dumps(DOWNLOADS_SIZES)
            return Py42Response(resp)

        storage_archive_client.create_file_size_job.side_effect = create_job
        storage_archive_client.get_file_size_job.side_effect = get_sizes
        storage_archive_client.get_file_size_job.side_effect = get_status
        poller = FileSizePoller(storage_archive_client, DEVICE_GUID)
        actual = poller.get_file_sizes([DESKTOP_ID, DOWNLOADS_ID], timeout=5000)
        assert actual[0]["numDirs"] == 1
        assert actual[0]["numFiles"] == 2
        assert actual[0]["size"] == 3
        assert actual[1]["numDirs"] == 4
        assert actual[1]["numFiles"] == 5
        assert actual[1]["size"] == 6


class TestRestoreJobManager(object):
    def test_restore_job_manager_constructs_successfully(self, storage_archive_client):
        assert RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

    def test_is_job_complete_with_incomplete_job_returns_false(
        self, mocker, storage_archive_client
    ):
        job_id = get_response_job_id(GetWebRestoreJobResponses.NOT_DONE)
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.NOT_DONE]
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        assert restore_job_manager.is_job_complete(job_id) is False

    def test_is_job_complete_with_complete_job_returns_complete(
        self, mocker, storage_archive_client
    ):
        job_id = get_response_job_id(GetWebRestoreJobResponses.DONE)
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        assert restore_job_manager.is_job_complete(job_id) is True

    def test_get_stream_calls_start_restore_with_correct_args(
        self, mocker, storage_archive_client, single_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(single_file_selection)
        storage_archive_client.start_restore.assert_called_once_with(
            guid=DEVICE_GUID,
            web_restore_session_id=WEB_RESTORE_SESSION_ID,
            path_set=[single_file_selection[0].path_set],
            num_files=1,
            num_dirs=1,
            size=1,
            show_deleted=True,
            zip_result=None,
        )

    def test_get_stream_when_multiple_files_selected_calls_start_restore_with_correct_args(
        self, mocker, storage_archive_client, double_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )

        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(double_file_selection)
        storage_archive_client.start_restore.assert_called_once_with(
            guid=DEVICE_GUID,
            web_restore_session_id=WEB_RESTORE_SESSION_ID,
            path_set=[
                double_file_selection[0].path_set,
                double_file_selection[1].path_set,
            ],
            num_files=1 + 4,
            num_dirs=2 + 5,
            size=3 + 6,
            show_deleted=True,
            zip_result=True,
        )

    def test_get_stream_polls_job_status_until_job_is_complete(
        self, mocker, storage_archive_client, single_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker,
            storage_archive_client,
            [
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.DONE,
            ],
        )

        restore_job_manager = RestoreJobManager(
            storage_archive_client,
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            job_polling_interval=0.000001,
        )
        restore_job_manager.get_stream(single_file_selection)
        job_id = get_response_job_id(GetWebRestoreJobResponses.DONE)
        expected_call = mocker.call(job_id)
        storage_archive_client.get_restore_status.assert_has_calls(
            [expected_call, expected_call, expected_call]
        )
        assert storage_archive_client.get_restore_status.call_count == 3

    def test_get_stream_when_successful_returns_response(
        self, mocker, storage_archive_client, single_file_selection, file_content_chunks
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )
        stream_restore_result_response_mock(
            mocker, storage_archive_client, file_content_chunks
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

        assert restore_job_manager.get_stream(single_file_selection)

    def test_get_stream_when_is_file_type_does_not_set_zip_result(
        self, mocker, storage_archive_client, single_file_selection, file_content_chunks
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )
        stream_restore_result_response_mock(
            mocker, storage_archive_client, file_content_chunks
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(single_file_selection)
        actual = storage_archive_client.start_restore.call_args[1]["zip_result"]
        assert actual is None

    def test_get_stream_when_is_directory_type_sets_zip_result_to_true(
        self, mocker, storage_archive_client, single_dir_selection, file_content_chunks
    ):
        mock_start_restore_response(
            mocker, storage_archive_client, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_client, [GetWebRestoreJobResponses.DONE]
        )
        stream_restore_result_response_mock(
            mocker, storage_archive_client, file_content_chunks
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_client, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(single_dir_selection)
        actual = storage_archive_client.start_restore.call_args[1]["zip_result"]
        assert actual is True
