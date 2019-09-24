import pytest
from requests import Response

from py42._internal.clients.security import SecurityClient, get_normalized_security_event_plan_info

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


@pytest.fixture
def security_client(mocker):
    return mocker.MagicMock(spec=SecurityClient)


@pytest.fixture
def response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.status_code = 200
    return response


@pytest.fixture
def security_client_one_location(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_LOCATION
    security_client.get_security_event_locations.return_value = response
    return security_client


@pytest.fixture
def security_client_two_plans_one_node(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_ONE_NODE
    security_client.get_security_event_locations.return_value = response
    return security_client


@pytest.fixture
def security_client_two_plans_two_nodes(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_NODES
    security_client.get_security_event_locations.return_value = response
    return security_client


@pytest.fixture
def security_client_one_plan_two_destinations(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_ONE_PLAN_TWO_DESTINATIONS
    security_client.get_security_event_locations.return_value = response
    return security_client


@pytest.fixture
def security_client_two_plans_two_destinations(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS
    security_client.get_security_event_locations.return_value = response
    return security_client


@pytest.fixture
def security_client_two_plans_two_destinations_three_nodes(security_client, response):
    response.text = GET_SECURITY_EVENT_LOCATIONS_RESPONSE_BODY_TWO_PLANS_TWO_DESTINATIONS_THREE_NODES
    security_client.get_security_event_locations.return_value = response
    return security_client


def test_get_normalized_security_event_plan_info_no_locations_response(security_client):
    security_client.get_security_event_locations.return_value = None
    plan_info = get_normalized_security_event_plan_info(security_client, USER_UID)
    assert plan_info == {}


def test_get_normalized_security_event_plan_info_one_location(security_client_one_location):
    plan_info = get_normalized_security_event_plan_info(security_client_one_location, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"}]}
    assert plan_info == expected


def test_get_normalized_security_event_plan_info_two_plans_one_node(security_client_two_plans_one_node):
    plan_info = get_normalized_security_event_plan_info(security_client_two_plans_one_node, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"}],
                "222222222222222222": [{"destinationGuid": "4", "nodeGuid": "41"}]}
    assert plan_info == expected


def test_get_normalized_security_event_plan_info_two_plans_two_nodes(security_client_two_plans_two_nodes):
    plan_info = get_normalized_security_event_plan_info(security_client_two_plans_two_nodes, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"}],
                "222222222222222222": [{"destinationGuid": "4", "nodeGuid": "42"}]}
    assert plan_info == expected


def test_get_normalized_security_event_plan_info_one_plan_two_destinations(security_client_one_plan_two_destinations):
    plan_info = get_normalized_security_event_plan_info(security_client_one_plan_two_destinations, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"},
                                       {"destinationGuid": "5", "nodeGuid": "51"}]}
    assert plan_info == expected


def test_get_normalized_security_event_plan_info_two_plans_two_destinations(security_client_two_plans_two_destinations):
    plan_info = get_normalized_security_event_plan_info(security_client_two_plans_two_destinations, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"},
                                       {"destinationGuid": "5", "nodeGuid": "51"}],
                "222222222222222222": [{"destinationGuid": "4", "nodeGuid": "41"},
                                       {"destinationGuid": "5", "nodeGuid": "51"}]}
    assert plan_info == expected


def test_get_normalized_security_event_plan_info_two_plans_two_destinations_three_nodes(security_client_two_plans_two_destinations_three_nodes):
    plan_info = get_normalized_security_event_plan_info(security_client_two_plans_two_destinations_three_nodes, USER_UID)
    expected = {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"},
                                       {"destinationGuid": "5", "nodeGuid": "51"}],
                "222222222222222222": [{"destinationGuid": "4", "nodeGuid": "41"},
                                       {"destinationGuid": "5", "nodeGuid": "52"}]}
    assert plan_info == expected
