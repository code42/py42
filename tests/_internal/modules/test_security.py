import pytest
from requests import Response

from py42._internal.client_factories import (
    FileEventClientFactory,
    StorageClientFactory,
    AlertClientFactory,
)
from py42._internal.clients.fileevent.file_event import FileEventClient
from py42._internal.clients.security import SecurityClient
from py42._internal.clients.storage.storage import StorageClient
from py42._internal.clients.storage.security import StorageSecurityClient
from py42._internal.modules.security import SecurityModule, PlanStorageInfo

RAW_QUERY = "RAW JSON QUERY"

USER_UID = "user-uid"

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_LOCATION = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_ONE_NODE = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_NODES = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_PLAN_TWO_DESTINATIONS = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""

GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS_THREE_NODES = """{
    "warnings": null,
    "data": {
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
    },
    "error": null
}"""


class TestSecurityModule(object):
    @pytest.fixture
    def security_client(self, mocker):
        return mocker.MagicMock(spec=SecurityClient)

    @pytest.fixture
    def response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        return response

    @pytest.fixture
    def security_client_one_location(self, security_client, response):
        response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_LOCATION
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def security_client_two_plans_one_node(self, security_client, response):
        response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_ONE_NODE
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def security_client_two_plans_two_nodes(self, security_client, response):
        response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_NODES
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def security_client_one_plan_two_destinations(self, security_client, response):
        response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_PLAN_TWO_DESTINATIONS
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def security_client_two_plans_two_destinations(self, security_client, response):
        response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def security_client_two_plans_two_destinations_three_nodes(self, security_client, response):
        response.text = (
            GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS_THREE_NODES
        )
        security_client.get_security_event_locations.return_value = response
        return security_client

    @pytest.fixture
    def storage_client_factory(self, mocker):
        return mocker.MagicMock(spec=StorageClientFactory)

    @pytest.fixture
    def file_event_client_factory(self, mocker):
        return mocker.MagicMock(spec=FileEventClientFactory)

    @pytest.fixture
    def alert_client_factory(self, mocker):
        return mocker.MagicMock(spec=AlertClientFactory)

    @pytest.fixture
    def file_event_client(self, mocker):
        return mocker.MagicMock(spec=FileEventClient)

    @staticmethod
    def return_file_event_client(file_event_client):
        def mock_get_file_event_client():
            return file_event_client

        return mock_get_file_event_client

    def test_search_file_events_with_only_query_calls_through_to_client(
        self,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        file_event_client,
        alert_client_factory,
    ):
        file_event_client_factory.get_file_event_client.side_effect = self.return_file_event_client(
            file_event_client
        )
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory, alert_client_factory
        )
        security_module.search_file_events(RAW_QUERY)
        file_event_client.search.assert_called_once_with(RAW_QUERY)

    def test_get_security_plan_storage_info_one_location_returns_location_info(
        self,
        security_client_one_location,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_one_location,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 1
        assert self._storage_info_contains(storage_infos, "111111111111111111", "4", "41")

    def test_get_security_plan_storage_info_two_plans_one_node_returns_both_location_info(
        self,
        security_client_two_plans_one_node,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_one_node,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 2
        assert self._storage_info_contains(storage_infos, "111111111111111111", "4", "41")
        assert self._storage_info_contains(storage_infos, "222222222222222222", "4", "41")

    def test_get_security_plan_storage_info_two_plans_two_nodes_returns_both_location_info(
        self,
        security_client_two_plans_two_nodes,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_nodes,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert self._storage_info_contains(storage_infos, "111111111111111111", "4", "41")
        assert self._storage_info_contains(storage_infos, "222222222222222222", "4", "42")

    def test_get_security_plan_storage_info_one_plan_two_destinations_returns_one_location(
        self,
        security_client_one_plan_two_destinations,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_one_plan_two_destinations,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_infos) == 1
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        ) or self._storage_info_contains(storage_infos, "111111111111111111", "5", "51")

    def test_get_security_plan_storage_info_two_plans_two_destinations_returns_one_location_per_plan(
        self,
        security_client_two_plans_two_destinations,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_destinations,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
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
        security_client_two_plans_two_destinations_three_nodes,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_destinations_three_nodes,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        storage_infos = security_module.get_security_plan_storage_info_list("foo")
        assert self._storage_info_contains(
            storage_infos, "111111111111111111", "4", "41"
        ) or self._storage_info_contains(storage_infos, "111111111111111111", "5", "51")
        assert self._storage_info_contains(
            storage_infos, "222222222222222222", "4", "41"
        ) or self._storage_info_contains(storage_infos, "222222222222222222", "5", "52")

    def test_get_user_security_events_calls_security_client_with_expected_params(
        self,
        mocker,
        security_client_one_location,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response = mocker.MagicMock(spec=Response)
        response.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.return_value = response
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client_one_location,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        for page, cursor in security_module.get_user_security_events("foo"):
            pass
        mock_storage_security_client.get_plan_security_events.assert_called_once_with(
            "111111111111111111",
            cursor=None,
            event_types=None,
            include_files=True,
            max_timestamp=None,
            min_timestamp=None,
        )

    def test_get_user_security_events_when_cursors_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client_one_location,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response1 = mocker.MagicMock(spec=Response)
        response1.text = '{"data": {"cursor": "1:1"}}'
        response2 = mocker.MagicMock(spec=Response)
        response2.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.side_effect = [
            response1,
            response2,
        ]
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client_one_location,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        for page, cursor in security_module.get_user_security_events("foo"):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 2

    def test_get_user_security_events_when_mutliple_plans_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client_two_plans_one_node,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response = mocker.MagicMock(spec=Response)
        response.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.return_value = response
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client_two_plans_one_node,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        for page, cursor in security_module.get_user_security_events("foo"):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 2

    def test_get_user_security_events_when_mutliple_plans_with_cursors_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client_two_plans_one_node,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response1 = mocker.MagicMock(spec=Response)
        response1.text = '{"data": {"cursor": "1:1"}}'
        response2 = mocker.MagicMock(spec=Response)
        response2.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.side_effect = [
            response1,
            response2,
            response1,
            response2,
        ]
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client_two_plans_one_node,
            storage_client_factory,
            file_event_client_factory,
            alert_client_factory,
        )
        for page, cursor in security_module.get_user_security_events("foo"):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 4

    def test_get_plan_security_events_calls_security_client_with_expected_params(
        self,
        mocker,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response = mocker.MagicMock(spec=Response)
        response.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.return_value = response
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory, alert_client_factory
        )
        for page, cursor in security_module.get_plan_security_events(
            PlanStorageInfo("111111111111111111", "41", "4")
        ):
            pass
        mock_storage_security_client.get_plan_security_events.assert_called_once_with(
            "111111111111111111",
            cursor=None,
            event_types=None,
            include_files=True,
            max_timestamp=None,
            min_timestamp=None,
        )

    def test_get_plan_security_events_when_cursors_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response1 = mocker.MagicMock(spec=Response)
        response1.text = '{"data": {"cursor": "1:1"}}'
        response2 = mocker.MagicMock(spec=Response)
        response2.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.side_effect = [
            response1,
            response2,
        ]
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory, alert_client_factory
        )
        for page, cursor in security_module.get_plan_security_events(
            PlanStorageInfo("111111111111111111", "41", "4")
        ):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 2

    def test_get_plan_security_events_when_mutliple_plans_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response = mocker.MagicMock(spec=Response)
        response.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.return_value = response
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory, alert_client_factory
        )
        plans = [
            PlanStorageInfo("111111111111111111", "41", "4"),
            PlanStorageInfo("222222222222222222", "41", "4"),
        ]
        for page, cursor in security_module.get_plan_security_events(plans):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 2

    def test_get_plan_security_events_when_mutliple_plans_with_cursors_returned_calls_security_client_expected_number_of_times(
        self,
        mocker,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        mock_storage_client = mocker.MagicMock(spec=StorageClient)
        mock_storage_security_client = mocker.MagicMock(spec=StorageSecurityClient)
        mock_storage_client.security = mock_storage_security_client
        response1 = mocker.MagicMock(spec=Response)
        response1.text = '{"data": {"cursor": "1:1"}}'
        response2 = mocker.MagicMock(spec=Response)
        response2.text = '{"data": {}}'
        mock_storage_security_client.get_plan_security_events.side_effect = [
            response1,
            response2,
            response1,
            response2,
        ]
        storage_client_factory.get_storage_client_from_plan_uid.return_value = mock_storage_client
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory, alert_client_factory
        )
        plans = [
            PlanStorageInfo("111111111111111111", "41", "4"),
            PlanStorageInfo("222222222222222222", "41", "4"),
        ]
        for page, cursor in security_module.get_plan_security_events(plans):
            pass
        assert mock_storage_security_client.get_plan_security_events.call_count == 4

    # the order the items are iterated through is not deterministic in some versions of python,
    # so we simply test that the value returned is one of the _possible_ values.
    def _storage_info_contains(self, storage_info_list, plan_uid, destination_guid, node_guid):
        return any(
            item.plan_uid == plan_uid
            and item.destination_guid == destination_guid
            and item.node_guid == node_guid
            for item in storage_info_list
        )
