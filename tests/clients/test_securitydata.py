import json

import pytest
from requests.exceptions import HTTPError

from py42.clients.securitydata import PlanStorageInfo
from py42.clients.securitydata import SecurityDataClient
from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.exceptions import Py42HTTPError
from py42.response import Py42Response
from py42.services.fileevent import FileEventService
from py42.services.preservationdata import PreservationDataService
from py42.services.savedsearch import SavedSearchService
from py42.services.securitydata import SecurityDataService
from py42.services.storage import StorageSecurityDataService
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.storage.preservationdata import StoragePreservationDataService

RAW_QUERY = "RAW JSON QUERY"
USER_UID = "user-uid"
PDS_EXCEPTION_MESSAGE = (
    u"No file with hash {0} available for download on any storage node."
)
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_LOCATION = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
    }"""
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_ONE_NODE = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111",
                            "222222222222222222"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
}"""
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_NODES = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111"
                        ]
                    },
                    {
                        "nodeGuid": "42",
                        "securityPlanUids": [
                            "222222222222222222"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
}"""
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_PLAN_TWO_DESTINATIONS = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111"
                        ]
                    }
                ]
            },
            {
                "destinationGuid": "5",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "51",
                        "securityPlanUids": [
                            "111111111111111111"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
}"""
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111",
                            "222222222222222222"
                        ]
                    }
                ]
            },
            {
                "destinationGuid": "5",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "51",
                        "securityPlanUids": [
                            "111111111111111111",
                            "222222222222222222"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
}"""
GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS_THREE_NODES = """{
        "securityPlanLocationsByDestination": [
            {
                "destinationGuid": "4",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "41",
                        "securityPlanUids": [
                            "111111111111111111",
                            "222222222222222222"
                        ]
                    }
                ]
            },
            {
                "destinationGuid": "5",
                "securityPlanLocationsByNode": [
                    {
                        "nodeGuid": "51",
                        "securityPlanUids": [
                            "111111111111111111"
                        ]
                    },
                    {
                        "nodeGuid": "52",
                        "securityPlanUids": [
                            "222222222222222222"
                        ]
                    }
                ]
            }
        ],
        "userUid": "917354657784339860"
}"""
FILE_EVENTS_RESPONSE = """{
    "fileEvents":[
        {
            "md5Checksum":"mdhash",
            "sha256Checksum":"shahash"
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
    "storageNodeURL": "https://host.com",
    "archiveGuid": "archiveid",
    "fileId": "fileid",
    "versionTimestamp": 12345
}"""


class TestSecurityModule(object):
    @pytest.fixture
    def security_service(self, mocker):
        return mocker.MagicMock(spec=SecurityDataService)

    @pytest.fixture
    def security_service_one_location(self, security_service, py42_response):
        py42_response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_LOCATION
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

    @pytest.fixture
    def security_service_two_plans_one_node(self, security_service, py42_response):
        py42_response.text = (
            GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_ONE_NODE
        )
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

    @pytest.fixture
    def security_service_two_plans_two_nodes(self, security_service, py42_response):
        py42_response.text = (
            GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_NODES
        )
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

    @pytest.fixture
    def security_service_one_plan_two_destinations(
        self, security_service, py42_response
    ):
        py42_response.text = (
            GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_PLAN_TWO_DESTINATIONS
        )
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

    @pytest.fixture
    def security_service_two_plans_two_destinations(
        self, security_service, py42_response
    ):
        py42_response.text = (
            GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS
        )
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

    @pytest.fixture
    def security_service_two_plans_two_destinations_three_nodes(
        self, security_service, py42_response
    ):
        py42_response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS_THREE_NODES
        security_service.get_security_event_locations.return_value = py42_response
        return security_service

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
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        security_module.search_file_events(RAW_QUERY)
        file_event_service.search.assert_called_once_with(RAW_QUERY)

    def test_get_security_plan_storage_info_one_location_returns_location_info(
        self,
        security_service_one_location,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_one_location,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 1
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        )

    def test_get_security_plan_storage_info_two_plans_one_node_returns_both_location_info(
        self,
        security_service_two_plans_one_node,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_two_plans_one_node,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 2
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        )
        assert self._storage_info_contains(
            storage_infos, "222222222222222222", "4", "41"
        )

    def test_get_security_plan_storage_info_two_plans_two_nodes_returns_both_location_info(
        self,
        security_service_two_plans_two_nodes,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_two_plans_two_nodes,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        )
        assert self._storage_info_contains(
            storage_infos, "222222222222222222", "4", "42"
        )

    def test_get_security_plan_storage_info_one_plan_two_destinations_returns_one_location(
        self,
        security_service_one_plan_two_destinations,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_one_plan_two_destinations,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 1
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        ) or self._storage_info_contains(storage_infos, "111111111111111111", "5", "51")

    def test_get_security_plan_storage_info_two_plans_two_destinations_returns_one_location_per_plan(
        self,
        security_service_two_plans_two_destinations,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_two_plans_two_destinations,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 2
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        ) or self._storage_info_contains(storage_infos, "111111111111111111", "5", "51")
        assert self._storage_info_contains(
            storage_infos, "222222222222222222", "4", "41"
        ) or self._storage_info_contains(storage_infos, "222222222222222222", "5", "51")

    def test_get_security_plan_storage_info_two_plans_two_destinations_three_nodes_returns_one_location_per_plan(
        self,
        security_service_two_plans_two_destinations_three_nodes,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service_two_plans_two_destinations_three_nodes,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        ) or self._storage_info_contains(storage_infos, "111111111111111111", "5", "51")
        assert self._storage_info_contains(
            storage_infos, "222222222222222222", "4", "41"
        ) or self._storage_info_contains(storage_infos, "222222222222222222", "5", "52")

    def test_get_all_user_security_events_calls_security_service_with_expected_params(
        self,
        mocker,
        security_service_one_location,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response = mocker.MagicMock(spec=Py42Response)
        response.text = "{}"
        mock_storage_security_service.get_plan_security_events.return_value = response
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service_one_location,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_user_security_events("foo"):
            pass
        mock_storage_security_service.get_plan_security_events.assert_called_once_with(
            "111111111111111111",
            cursor=None,
            event_types=None,
            include_files=True,
            max_timestamp=None,
            min_timestamp=None,
        )

    def test_get_all_user_security_events_when_cursors_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service_one_location,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response1 = mocker.MagicMock(spec=Py42Response)
        response1.text = '{"cursor": "1:1"}'
        response2 = mocker.MagicMock(spec=Py42Response)
        response2.text = "{}"
        mock_storage_security_service.get_plan_security_events.side_effect = [
            response1,
            response2,
        ]
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service_one_location,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_user_security_events("foo"):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 2

    def test_get_all_user_security_events_when_multiple_plans_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service_two_plans_one_node,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response = mocker.MagicMock(spec=Py42Response)
        response.text = "{}"
        mock_storage_security_service.get_plan_security_events.return_value = response
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service_two_plans_one_node,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_user_security_events("foo"):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 2

    def test_get_all_user_security_events_when_multiple_plans_with_cursors_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service_two_plans_one_node,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response1 = mocker.MagicMock(spec=Py42Response)
        response1.text = '{"cursor": "1:1"}'
        response2 = mocker.MagicMock(spec=Py42Response)
        response2.text = "{}"
        mock_storage_security_service.get_plan_security_events.side_effect = [
            response1,
            response2,
            response1,
            response2,
        ]
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service_two_plans_one_node,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_user_security_events("foo"):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 4

    @pytest.mark.parametrize(
        "plan_storage_info",
        [
            PlanStorageInfo("111111111111111111", "41", "4"),
            (PlanStorageInfo("111111111111111111", "41", "4"),),
            [PlanStorageInfo("111111111111111111", "41", "4")],
        ],
    )
    def test_get_all_plan_security_events_calls_security_service_with_expected_params(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        plan_storage_info,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response = mocker.MagicMock(spec=Py42Response)
        response.text = "{}"
        mock_storage_security_service.get_plan_security_events.return_value = response
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_plan_security_events(plan_storage_info):
            pass
        mock_storage_security_service.get_plan_security_events.assert_called_once_with(
            "111111111111111111",
            cursor=None,
            event_types=None,
            include_files=True,
            max_timestamp=None,
            min_timestamp=None,
        )

    def test_get_all_plan_security_events_when_cursors_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response1 = mocker.MagicMock(spec=Py42Response)
        response1.text = '{"cursor": "1:1"}'
        response2 = mocker.MagicMock(spec=Py42Response)
        response2.text = "{}"
        mock_storage_security_service.get_plan_security_events.side_effect = [
            response1,
            response2,
        ]
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        for _, _ in security_module.get_all_plan_security_events(
            PlanStorageInfo("111111111111111111", "41", "4")
        ):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 2

    def test_get_all_plan_security_events_when_multiple_plans_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response = mocker.MagicMock(spec=Py42Response)
        response.text = "{}"
        mock_storage_security_service.get_plan_security_events.return_value = response
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        plans = [
            PlanStorageInfo("111111111111111111", "41", "4"),
            PlanStorageInfo("222222222222222222", "41", "4"),
        ]
        for _, _ in security_module.get_all_plan_security_events(plans):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 2

    def test_get_all_plan_security_events_when_multiple_plans_with_cursors_returned_calls_security_service_expected_number_of_times(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        mock_storage_security_service = mocker.MagicMock(
            spec=StorageSecurityDataService
        )
        response1 = mocker.MagicMock(spec=Py42Response)
        response1.text = '{"cursor": "1:1"}'
        response2 = mocker.MagicMock(spec=Py42Response)
        response2.text = "{}"
        mock_storage_security_service.get_plan_security_events.side_effect = [
            response1,
            response2,
            response1,
            response2,
        ]
        storage_service_factory.create_security_data_service.return_value = (
            mock_storage_security_service
        )
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        plans = [
            PlanStorageInfo("111111111111111111", "41", "4"),
            PlanStorageInfo("222222222222222222", "41", "4"),
        ]
        for _, _ in security_module.get_all_plan_security_events(plans):
            pass
        assert mock_storage_security_service.get_plan_security_events.call_count == 4

    # the order the items are iterated through is not deterministic in some versions of python,
    # so we simply test that the value returned is one of the _possible_ values.
    def _storage_info_contains(
        self, storage_info_list, plan_uid, destination_guid, node_guid
    ):
        return any(
            item.plan_uid == plan_uid
            and item.destination_guid == destination_guid
            and item.node_guid == node_guid
            for item in storage_info_list
        )

    def test_saved_searches_returns_saved_search_client(
        self,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )
        assert security_module.savedsearches

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
    def find_file_version(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        pds_file_version_response = response
        pds_file_version_response.text = PDS_FILE_VERSIONS
        return pds_file_version_response

    @pytest.fixture
    def file_download(self, mocker):
        response = mocker.MagicMock(spec=Py42Response)
        response.status_code = 200
        response.encoding = None
        response.__getitem__ = lambda _, key: json.loads(response.text).get(key)
        download_token_response = response
        download_token_response.text = "PDSDownloadToken=token"
        return download_token_response

    def test_stream_file_by_sha256_returns_stream_of_file(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
        file_download,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        preservation_data_service.find_file_versions.return_value = find_file_version
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_module.stream_file_by_sha256("shahash")
        assert response == b"stream"

    def test_stream_file_by_sha256_raises_py42_checksum_not_found_error_when_search_returns_empty_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
    ):
        file_event_search.text = "{}"
        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_module.stream_file_by_sha256("shahash")

        assert u"No files found with SHA256 checksum" in e.value.args[0]

    def test_stream_file_by_sha256_raises_file_not_found_error_when_file_location_returns_empty_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_location.text = """{"locations": []}"""
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_sha256("shahash")
        assert u"PDS service can't find requested file" in e.value.args[0]

    def test_stream_file_by_sha256_raises_py42_error_when_find_file_versions_returns_204_status_code(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
    ):
        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        preservation_data_service = mocker.MagicMock(spec=PreservationDataService)
        find_file_version.status_code = 204
        preservation_data_service.find_file_versions.return_value = find_file_version

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_sha256("shahash")

        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("shahash")

    def test_stream_file_by_sha256_raises_py42_error_when_file_download_returns_failure_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
        file_download,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        preservation_data_service.find_file_versions.return_value = find_file_version
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.side_effect = Py42HTTPError(HTTPError())
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_sha256("shahash")
        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("shahash")

    def test_stream_file_by_md5_returns_stream_of_file(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
        file_download,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        preservation_data_service.find_file_versions.return_value = find_file_version
        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.return_value = b"stream"
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        response = security_module.stream_file_by_md5("md5hash")
        assert response == b"stream"

    def test_stream_file_by_md5_raises_py42_checksum_not_found_error_when_search_returns_empty_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
    ):

        file_event_search.text = "{}"
        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42ChecksumNotFoundError) as e:
            security_module.stream_file_by_md5("md5hash")
        assert u"No files found with MD5 checksum" in e.value.args[0]

    def test_stream_file_by_md5_raises_file_not_found_error_when_file_location_returns_empty_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_location.text = """{"locations": []}"""
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_md5("md5hash")
        assert u"PDS service can't find requested file" in e.value.args[0]

    def test_stream_file_by_md5_raises_py42_error_when_find_file_versions_returns_204_status_code(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
    ):

        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )
        find_file_version.status_code = 204
        preservation_data_service.find_file_versions.return_value = find_file_version

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_md5("md5hash")
        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("md5hash")

    def test_stream_file_by_md5_raises_py42_error_when_file_download_returns_failure_response(
        self,
        mocker,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
        file_event_search,
        file_location,
        find_file_version,
        file_download,
    ):
        file_event_service = mocker.MagicMock(spec=FileEventService)
        file_event_service.search.return_value = file_event_search
        file_event_service.get_file_location_detail_by_sha256.return_value = (
            file_location
        )

        preservation_data_service.find_file_versions.return_value = find_file_version

        storage_node_client = mocker.MagicMock(spec=StoragePreservationDataService)
        storage_node_client.get_download_token.return_value = file_download
        storage_node_client.get_file.side_effect = Py42HTTPError(HTTPError())
        storage_service_factory.create_preservation_data_service.return_value = (
            storage_node_client
        )

        security_module = SecurityDataClient(
            security_service,
            file_event_service,
            preservation_data_service,
            saved_search_service,
            storage_service_factory,
        )

        with pytest.raises(Py42Error) as e:
            security_module.stream_file_by_md5("md5hash")
        assert e.value.args[0] == PDS_EXCEPTION_MESSAGE.format("md5hash")
