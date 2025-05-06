import pytest
import requests
from tests.conftest import create_mock_response

from py42.clients.securitydata import SecurityDataClient
from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.services._connection import Connection
from py42.services.fileevent import FileEventService
from py42.services.preservationdata import PreservationDataService
from py42.services.savedsearch import SavedSearchService
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.storage.exfiltrateddata import ExfiltratedDataService

FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
RAW_QUERY = "RAW JSON QUERY"
USER_UID = "user-uid"
PDS_EXCEPTION_MESSAGE = "No file with hash {0} available for download."
FILE_EVENTS_RESPONSE_V2 = """{
    "fileEvents":[
        {
            "@timestamp": "1",
            "user": { "deviceUid": "testdeviceUid" },
            "file": { "name": "testfileName", "directory": "/test/file/path/",
                "hash": { "md5": "testmd5-2", "sha256": "testsha256-2" }
            }
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


XFC_EXACT_FILE_VERSION_RESPONSE = """{
    "match": {
        "downloadTokenRequest": "https://test-url/test-path?token=test-token"
    }
}"""

XFC_NOT_FOUND_RESPONSE = """{
    "match": null,
    "failureReports": [
        "failure-one"
    ]
}"""


class TestSecurityClient:
    @pytest.fixture
    def connection(self, mocker):
        connection = mocker.MagicMock(spec=Connection)
        connection._session = mocker.MagicMock(spec=requests.Session)
        return connection

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
        return create_mock_response(mocker, FILE_EVENTS_RESPONSE_V2)

    @pytest.fixture
    def file_event_search_v2(self, mocker):
        return create_mock_response(mocker, FILE_EVENTS_RESPONSE_V2)

    @pytest.fixture
    def file_location(self, mocker):
        return create_mock_response(mocker, FILE_LOCATION_RESPONSE)

    @pytest.fixture
    def file_version_list(self, mocker):
        return create_mock_response(mocker, XFC_EXACT_FILE_VERSION_RESPONSE)

    @pytest.fixture
    def empty_file_versions(self, mocker):
        return create_mock_response(mocker, XFC_NOT_FOUND_RESPONSE)

    @pytest.fixture
    def pds_config(
        self,
        mocker,
        storage_service_factory,
        file_event_service,
        preservation_data_service,
        saved_search_service,
    ):
        mock = mocker.MagicMock()
        file_event_service.search.return_value = create_mock_response(
            mocker, FILE_EVENTS_RESPONSE_V2
        )
        preservation_data_service.get_file_version_list.return_value = (
            create_mock_response(mocker, XFC_EXACT_FILE_VERSION_RESPONSE)
        )
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            create_mock_response(mocker, FILE_LOCATION_RESPONSE)
        )
        exfiltration_client = mocker.MagicMock(spec=ExfiltratedDataService)
        exfiltration_client.get_file.return_value = b"stream"
        storage_service_factory.create_exfiltrated_data_service.return_value = (
            exfiltration_client
        )

        mock.storage_service_factory = storage_service_factory
        mock.file_event_service = file_event_service
        mock.preservation_data_service = preservation_data_service
        mock.saved_search_service = saved_search_service
        mock.exfiltration_client = exfiltration_client
        return mock

    @pytest.fixture
    def pds_config_v2(
        self,
        mocker,
        storage_service_factory,
        file_event_service,
        preservation_data_service,
        saved_search_service,
    ):
        mock = mocker.MagicMock()
        file_event_service.search.return_value = create_mock_response(
            mocker, FILE_EVENTS_RESPONSE_V2
        )
        preservation_data_service.get_file_version_list.return_value = (
            create_mock_response(mocker, XFC_EXACT_FILE_VERSION_RESPONSE)
        )
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            create_mock_response(mocker, FILE_LOCATION_RESPONSE)
        )
        exfiltration_client = mocker.MagicMock(spec=ExfiltratedDataService)
        exfiltration_client.get_file.return_value = b"stream"
        storage_service_factory.create_exfiltrated_data_service.return_value = (
            exfiltration_client
        )

        mock.storage_service_factory = storage_service_factory
        mock.file_event_service = file_event_service
        mock.preservation_data_service = preservation_data_service
        mock.saved_search_service = saved_search_service
        mock.exfiltration_client = exfiltration_client
        return mock

    def test_stream_file_by_sha256_with_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        pds_config,
    ):

        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )

        response = security_client.stream_file_by_sha256("testsha256-2")
        version_list_params = [
            "testdeviceUid",
            "testmd5-2",
            "testsha256-2",
            "/test/file/path/testfileName",
        ]
        pds_config.preservation_data_service.get_file_version_list.assert_called_once_with(
            *version_list_params
        )
        pds_config.storage_service_factory.create_exfiltrated_data_service.assert_called_once_with(
            "https://test-url"
        )
        assert (
            pds_config.file_event_service.get_file_location_detail_by_sha256.call_count
            == 0
        )
        assert response == b"stream"

    def test_stream_file_by_sha256_when_search_returns_empty_response_raises_py42_checksum_not_found_error_(
        self, mocker, pds_config
    ):
        pds_config.file_event_service.search.return_value = create_mock_response(
            mocker, '{"fileEvents": []}'
        )
        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_client.stream_file_by_sha256("shahash")

        assert "No files found with SHA256 checksum" in e.value.args[0]

    def test_stream_file_by_sha256_when_get_locations_returns_empty_list_raises_py42_error(
        self, mocker, pds_config, empty_file_versions
    ):
        file_location = create_mock_response(mocker, '{"locations": []}')
        pds_config.preservation_data_service.get_file_version_list.return_value = (
            empty_file_versions
        )
        pds_config.file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_client.stream_file_by_sha256("shahash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("shahash")

    def test_stream_file_by_md5_with_exact_match_response_calls_get_version_list_with_expected_params(
        self,
        pds_config,
    ):
        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )

        response = security_client.stream_file_by_md5("testmd5-2")
        version_list_params = [
            "testdeviceUid",
            "testmd5-2",
            "testsha256-2",
            "/test/file/path/testfileName",
        ]
        pds_config.preservation_data_service.get_file_version_list.assert_called_once_with(
            *version_list_params
        )
        pds_config.storage_service_factory.create_exfiltrated_data_service.assert_called_once_with(
            "https://test-url"
        )
        assert (
            pds_config.file_event_service.get_file_location_detail_by_sha256.call_count
            == 0
        )
        assert response == b"stream"

    def test_stream_file_by_md5_when_search_returns_empty_response_raises_py42_checksum_not_found_error_(
        self,
        mocker,
        pds_config,
    ):
        pds_config.file_event_service.search.return_value = create_mock_response(
            mocker, '{"fileEvents": []}'
        )
        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_client.stream_file_by_md5("mdhash")

        assert "No files found with MD5 checksum" in e.value.args[0]

    def test_stream_file_by_md5_when_has_exact_match_calls_get_token_with_expected_params_and_streams_successfully(
        self, mocker, pds_config
    ):
        file_version_list = create_mock_response(
            mocker, XFC_EXACT_FILE_VERSION_RESPONSE
        )
        pds_config.preservation_data_service.get_file_version_list.return_value = (
            file_version_list
        )

        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )
        response = security_client.stream_file_by_md5("testmd5-2")
        assert response == b"stream"

    def test_stream_file_by_sha256_when_has_exact_match_calls_get_token_with_expected_params_and_streams_successfully(
        self, mocker, pds_config
    ):
        file_version_list = create_mock_response(
            mocker, XFC_EXACT_FILE_VERSION_RESPONSE
        )
        pds_config.preservation_data_service.get_file_version_list.return_value = (
            file_version_list
        )

        security_client = SecurityDataClient(
            pds_config.file_event_service,
            pds_config.preservation_data_service,
            pds_config.saved_search_service,
            pds_config.storage_service_factory,
        )
        response = security_client.stream_file_by_sha256("testsha256-2")
        assert response == b"stream"

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
            "pgSize": 500,
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
            "pgSize": 500,
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
            "pgSize": 500,
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
            "pgSize": 500,
        }
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)

    def test_search_all_file_events_when_token_is_none_succeeds(
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
        security_client.search_all_file_events(FileEventQuery.all(), page_token=None)
