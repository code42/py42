import json

import pytest

from py42.clients.securitydata import SecurityDataClient
from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.response import Py42Response
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.services._connection import Connection
from py42.services.fileevent import FileEventService
from py42.services.preservationdata import PreservationDataService
from py42.services.savedsearch import SavedSearchService
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.storage.preservationdata import StoragePreservationDataService

FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
RAW_QUERY = "RAW JSON QUERY"
USER_UID = "user-uid"
PDS_EXCEPTION_MESSAGE = (
    "No file with hash {0} available for download on any storage node."
)
FILE_EVENTS_RESPONSE = """{
    "fileEvents":[
        {
            "deviceUid": "testdeviceUid",
            "fileName": "testfileName",
            "filePath": "/test/file/path/",
            "md5Checksum":"testmd5-2",
            "sha256Checksum":"testsha256-2"
        }
    ]
}"""
FILE_LOCATION_RESPONSE = """{
    "locations": [
        {
            "fileName": "file1",
            "deviceUid": "device1",
            "filePath": "path1"
        },
        {
            "fileName": "file2",
            "deviceUid": "device2",
            "filePath": "path2"
        }
    ]
}"""
PDS_FILE_VERSIONS = """{
    "versions": [
        {
            "storageNodeURL": "https://host-1.com",
            "archiveGuid": "archiveid-1",
            "fileId": "fileid-1",
            "fileMD5": "testmd5-1",
            "fileSHA256": "testsha256-1",
            "versionTimestamp": 12345
        },
        {
            "storageNodeURL": "https://host-2.com",
            "archiveGuid": "archiveid-2",
            "fileId": "fileid-2",
            "fileMD5": "testmd5-2",
            "fileSHA256": "testsha256-2",
            "versionTimestamp": 12344
        },
        {
            "storageNodeURL": "https://host-3.com",
            "archiveGuid": "archiveid-3",
            "fileId": "fileid-3",
            "fileMD5": "testmd5-3",
            "fileSHA256": "testsha256-3",
            "versionTimestamp": 12346
        }
    ]
}"""

AVAILABLE_VERSION_RESPONSE = """{
    "storageNodeURL": "https://host.com",
    "archiveGuid": "archiveid-3",
    "fileId": "fileid-3",
    "fileMD5": "testmd5-3",
    "fileSHA256": "testsha256-3",
    "versionTimestamp": 12346
}"""


class TestSecurityClient(object):
    @pytest.fixture
    def connection(self, mocker):
        return mocker.MagicMock(spec=Connection)

    @pytest.fixture
    def storage_service_factory(self, mocker):
        return mocker.MagicMock(spec=StorageServiceFactory)

    @pytest.fixture
    def file_event_service(self, mocker):
        return mocker.MagicMock(spec=FileEventService)

    @pytest.fixture
    def preservation_data_service(self, mocker):
        return mocker.MagicMock(spec=PreservationDataService)

    @pytest.fixture
    def saved_search_service(self, mocker):
        return mocker.MagicMock(spec=SavedSearchService)

    def test_search_with_only_query_calls_through_to_client(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        security_client.search_file_events(RAW_QUERY)
        file_event_service.search.assert_called_once_with(RAW_QUERY)

    def test_saved_searches_returns_saved_search_client(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        assert security_client.savedsearches

    @pytest.fixture
    def file_event_search(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        file_event_response = response
        file_event_response.text = FILE_EVENTS_RESPONSE
        return file_event_response

    @pytest.fixture
    def file_location(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        file_location_response = response
        file_location_response.text = FILE_LOCATION_RESPONSE
        return file_location_response

    @pytest.fixture
    def file_version_list(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        pds_file_version_response = response
        pds_file_version_response.text = PDS_FILE_VERSIONS
        return pds_file_version_response

    @pytest.fixture
    def available_version(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        available_version_response = response
        available_version_response.text = AVAILABLE_VERSION_RESPONSE
        return available_version_response

    @pytest.fixture
    def file_download(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        download_token_response = response
        download_token_response.text = "PDSDownloadToken=token"
        return download_token_response

    def test_stream_file_by_sha256_with_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_download,
    ):
        file_event_service.search.return_value = file_event_search
        preservation_data_service.get_file_version_list.return_value = file_version_list
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_client.stream_file_by_sha256("testsha256-2")
        version_list_params = [
            "testdeviceUid",
            "testmd5-2",
            "testsha256-2",
            "/test/file/path/testfileName",
        ]
        preservation_data_service.get_file_version_list.assert_called_once_with(
            *version_list_params
        )
        storage_service_factory.create_preservation_data_service.assert_called_once_with(
            "https://host-2.com"
        )
        assert file_event_service.get_file_location_detail_by_sha256.call_count == 0
        assert preservation_data_service.find_file_version.call_count == 0
        download_token_params = ["archiveid-2", "fileid-2", 12344]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )
        assert response == b"stream"

    def test_stream_file_by_sha256_without_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_download,
    ):
        file_event_search.text = file_event_search.text.replace("-2", "-6")
        file_event_service.search.return_value = file_event_search
        preservation_data_service.get_file_version_list.return_value = file_version_list
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_client.stream_file_by_sha256("testsha256-6")
        expected = [
            "testdeviceUid",
            "testmd5-6",
            "testsha256-6",
            "/test/file/path/testfileName",
        ]
        preservation_data_service.get_file_version_list.assert_called_once_with(
            *expected
        )
        storage_service_factory.create_preservation_data_service.assert_called_once_with(
            "https://host-3.com"
        )
        assert file_event_service.get_file_location_detail_by_sha256.call_count == 0
        assert preservation_data_service.find_file_version.call_count == 0
        # should get version with most recent versionTimestamp
        download_token_params = ["archiveid-3", "fileid-3", 12346]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )
        assert response == b"stream"

    def test_stream_file_by_sha256_when_search_returns_empty_response_raises_py42_checksum_not_found_error_(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
    ):
        file_event_search.text = '{"fileEvents": []}'
        file_event_service.search.return_value = file_event_search
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_client.stream_file_by_sha256("shahash")

        assert "No files found with SHA256 checksum" in e.value.args[0]

    def test_stream_file_by_sha256_when_file_versions_returns_empty_response_gets_version_from_other_location(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_location,
        file_download,
        available_version,
    ):
        file_version_list.text = '{"versions": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        preservation_data_service.find_file_version.return_value = available_version
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )

        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        response = security_client.stream_file_by_sha256("shahash")
        assert response == b"stream"
        file_event_service.get_file_location_detail_by_sha256.assert_called_once_with(
            "testsha256-2"
        )
        expected = ["testmd5-2", "testsha256-2", mocker.ANY]
        preservation_data_service.find_file_version.assert_called_once_with(*expected)
        # should return version returned by find_file_version
        download_token_params = ["archiveid-3", "fileid-3", 12346]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )

    def test_stream_file_by_sha256_when_get_locations_returns_empty_list_raises_py42_error(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_location,
    ):
        file_version_list.text = '{"versions": []}'
        file_location.text = '{"locations": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_client.stream_file_by_sha256("shahash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("shahash")

    def test_stream_file_by_sha256_when_find_file_version_returns_204_status_code_raises_py42_error(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        file_version_list,
        available_version,
    ):
        file_version_list.text = '{"versions": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        available_version.status_code = 204
        preservation_data_service.find_file_version.return_value = available_version

        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_client.stream_file_by_sha256("shahash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("shahash")

    def test_stream_file_by_md5_with_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_download,
    ):
        file_event_service.search.return_value = file_event_search
        preservation_data_service.get_file_version_list.return_value = file_version_list
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_client.stream_file_by_md5("testmd5-2")
        version_list_params = [
            "testdeviceUid",
            "testmd5-2",
            "testsha256-2",
            "/test/file/path/testfileName",
        ]
        preservation_data_service.get_file_version_list.assert_called_once_with(
            *version_list_params
        )
        storage_service_factory.create_preservation_data_service.assert_called_once_with(
            "https://host-2.com"
        )
        assert file_event_service.get_file_location_detail_by_sha256.call_count == 0
        assert preservation_data_service.find_file_version.call_count == 0
        download_token_params = ["archiveid-2", "fileid-2", 12344]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )
        assert response == b"stream"

    def test_stream_file_by_md5_without_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_download,
    ):
        file_event_search.text = file_event_search.text.replace("-2", "-6")
        file_event_service.search.return_value = file_event_search
        preservation_data_service.get_file_version_list.return_value = file_version_list
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_client.stream_file_by_md5("testmd5-6")
        expected = [
            "testdeviceUid",
            "testmd5-6",
            "testsha256-6",
            "/test/file/path/testfileName",
        ]
        preservation_data_service.get_file_version_list.assert_called_once_with(
            *expected
        )
        storage_service_factory.create_preservation_data_service.assert_called_once_with(
            "https://host-3.com"
        )
        assert file_event_service.get_file_location_detail_by_sha256.call_count == 0
        assert preservation_data_service.find_file_version.call_count == 0
        # should get version returned with most recent versionTimestamp
        download_token_params = ["archiveid-3", "fileid-3", 12346]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )
        assert response == b"stream"

    def test_stream_file_by_md5_when_search_returns_empty_response_raises_py42_checksum_not_found_error_(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
    ):
        file_event_search.text = '{"fileEvents": []}'
        file_event_service.search.return_value = file_event_search
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_client.stream_file_by_md5("mdhash")

        assert "No files found with MD5 checksum" in e.value.args[0]

    def test_stream_file_by_md5_when_file_versions_returns_empty_response_gets_version_from_other_location(
        self,
        mocker,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_location,
        file_download,
        available_version,
    ):
        file_version_list.text = '{"versions": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        preservation_data_service.find_file_version.return_value = available_version
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )

        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        response = security_client.stream_file_by_md5("mdhash")
        assert response == b"stream"
        file_event_service.get_file_location_detail_by_sha256.assert_called_once_with(
            "testsha256-2"
        )
        expected = ["testmd5-2", "testsha256-2", mocker.ANY]
        preservation_data_service.find_file_version.assert_called_once_with(*expected)
        # should return version returned by find_file_version
        download_token_params = ["archiveid-3", "fileid-3", 12346]
        storage_node_client.get_download_token.assert_called_once_with(
            *download_token_params
        )

    def test_stream_file_by_md5_when_get_locations_returns_empty_list_raises_py42_error(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_version_list,
        file_location,
    ):
        file_version_list.text = '{"versions": []}'
        file_location.text = '{"locations": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_client.stream_file_by_md5("mdhash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("mdhash")

    def test_stream_file_by_md5_when_find_file_version_returns_204_status_code_raises_py42_error(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        file_version_list,
        available_version,
    ):
        file_version_list.text = '{"versions": []}'
        preservation_data_service.get_file_version_list.return_value = file_version_list
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        available_version.status_code = 204
        preservation_data_service.find_file_version.return_value = available_version

        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_client.stream_file_by_md5("mdhash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("mdhash")

    def test_search_all_file_events_calls_search_with_expected_params_when_pg_token_is_not_passed(
        self,
        connection,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        file_event_service = FileEventService(connection)
        successful_response = {
            "totalCount": None,
            "fileEvents": None,
            "nextPgToken": None,
            "problems": None,
        }
        connection.post.return_value = successful_response

        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        query = FileEventQuery.all()
        response = security_client.search_all_file_events(query)
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": "",
            "pgSize": 10000,
        }
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
        assert response is successful_response

    def test_search_all_file_events_calls_search_with_expected_params_when_pg_token_is_passed(
        self,
        connection,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        file_event_service = FileEventService(connection)
        successful_response = {
            "totalCount": None,
            "fileEvents": None,
            "nextPgToken": "pqr",
            "problems": None,
        }
        connection.post.return_value = successful_response
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        query = FileEventQuery.all()
        response = security_client.search_all_file_events(query, "abc")
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": "abc",
            "pgSize": 10000,
        }
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
        assert response is successful_response

    def test_search_all_file_events_handles_unescaped_quote_chars_in_token(
        self,
        connection,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        file_event_service = FileEventService(connection)
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        unescaped_token = '1234_"abcde"'
        escaped_token = r"1234_\"abcde\""
        security_client.search_all_file_events(FileEventQuery.all(), unescaped_token)
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": escaped_token,
            "pgSize": 10000,
        }
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)

    def test_search_all_file_events_handles_escaped_quote_chars_in_token(
        self,
        connection,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        file_event_service = FileEventService(connection)
        security_client = SecurityDataClient(
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        escaped_token = r"1234_\"abcde\""
        security_client.search_all_file_events(FileEventQuery.all(), escaped_token)
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": escaped_token,
            "pgSize": 10000,
        }
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
