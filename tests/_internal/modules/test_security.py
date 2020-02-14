import pytest
from requests import Response

from py42._internal.client_factories import FileEventClientFactory, StorageClientFactory
from py42._internal.clients.fileevent.file_event import FileEventClient
from py42._internal.clients.security import SecurityClient
from py42._internal.modules.security import SecurityModule

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
    def file_event_client(self, mocker):
        return mocker.MagicMock(spec=FileEventClient)

    @staticmethod
    def return_file_event_client(file_event_client):
        def mock_get_file_event_client():
            return file_event_client

        return mock_get_file_event_client

    def test_search_file_events_with_only_query_calls_through_to_client(
        self, security_client, storage_client_factory, file_event_client_factory, file_event_client
    ):
        file_event_client_factory.get_file_event_client.side_effect = self.return_file_event_client(
            file_event_client
        )
        security_module = SecurityModule(
            security_client, storage_client_factory, file_event_client_factory
        )
        security_module.search_file_events(RAW_QUERY)
        file_event_client.search_file_events.assert_called_once_with(RAW_QUERY)

    def test_get_security_plan_storage_info_one_location_returns_location_info(
        self, security_client_one_location, storage_client_factory, file_event_client_factory
    ):
        security_module = SecurityModule(
            security_client_one_location, storage_client_factory, file_event_client_factory
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 1
        assert storage_info_list[0].node_guid == "41"
        assert storage_info_list[0].destination_guid == "4"
        assert storage_info_list[0].plan_uid == "111111111111111111"

    def test_get_security_plan_storage_info_two_plans_one_node_returns_both_location_info(
        self, security_client_two_plans_one_node, storage_client_factory, file_event_client_factory
    ):
        security_module = SecurityModule(
            security_client_two_plans_one_node, storage_client_factory, file_event_client_factory
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 2
        assert storage_info_list[0].node_guid == "41"
        assert storage_info_list[0].destination_guid == "4"
        assert storage_info_list[0].plan_uid == "111111111111111111"
        assert storage_info_list[1].node_guid == "41"
        assert storage_info_list[1].destination_guid == "4"
        assert storage_info_list[1].plan_uid == "222222222222222222"

    def test_get_security_plan_storage_info_two_plans_two_nodes_returns_both_location_info(
        self, security_client_two_plans_two_nodes, storage_client_factory, file_event_client_factory
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_nodes, storage_client_factory, file_event_client_factory
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 2
        assert storage_info_list[0].node_guid == "41"
        assert storage_info_list[0].destination_guid == "4"
        assert storage_info_list[0].plan_uid == "111111111111111111"
        assert storage_info_list[1].node_guid == "42"
        assert storage_info_list[1].destination_guid == "4"
        assert storage_info_list[1].plan_uid == "222222222222222222"

    def test_get_security_plan_storage_info_one_plan_two_destinations_returns_one_location(
        self,
        security_client_one_plan_two_destinations,
        storage_client_factory,
        file_event_client_factory,
    ):
        security_module = SecurityModule(
            security_client_one_plan_two_destinations,
            storage_client_factory,
            file_event_client_factory,
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 1
        assert storage_info_list[0].node_guid == "51"
        assert storage_info_list[0].destination_guid == "5"
        assert storage_info_list[0].plan_uid == "111111111111111111"

    def test_get_security_plan_storage_info_two_plans_two_destinations_returns_one_location_per_plan(
        self,
        security_client_two_plans_two_destinations,
        storage_client_factory,
        file_event_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_destinations,
            storage_client_factory,
            file_event_client_factory,
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 2
        assert storage_info_list[0].node_guid == "51"
        assert storage_info_list[0].destination_guid == "5"
        assert storage_info_list[0].plan_uid == "111111111111111111"
        assert storage_info_list[1].node_guid == "51"
        assert storage_info_list[1].destination_guid == "5"
        assert storage_info_list[1].plan_uid == "222222222222222222"

    def test_get_security_plan_storage_info_two_plans_two_destinations_three_nodes_returns_one_location_per_plan(
        self,
        security_client_two_plans_two_destinations_three_nodes,
        storage_client_factory,
        file_event_client_factory,
    ):
        security_module = SecurityModule(
            security_client_two_plans_two_destinations_three_nodes,
            storage_client_factory,
            file_event_client_factory,
        )
        storage_info_list = security_module.get_security_plan_storage_info_list("foo")
        assert len(storage_info_list) == 2
        assert storage_info_list[0].node_guid == "51"
        assert storage_info_list[0].destination_guid == "5"
        assert storage_info_list[0].plan_uid == "111111111111111111"
        assert storage_info_list[1].node_guid == "52"
        assert storage_info_list[1].destination_guid == "5"
        assert storage_info_list[1].plan_uid == "222222222222222222"

    # def test_get_normalized_security_event_plan_info_no_locations_response(security_client):
    #     security_client.get_security_event_locations.return_value = None
    #     plan_info = get_normalized_security_event_plan_info(security_client, USER_UID)
    #     assert plan_info == {}
    #
