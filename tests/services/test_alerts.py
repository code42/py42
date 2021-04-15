import json

import pytest
from requests import Response
from tests.conftest import TENANT_ID_FROM_RESPONSE

from py42.response import Py42Response
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import AlertState
from py42.services._connection import Connection
from py42.services.alerts import AlertService

TEST_RESPONSE = """
{"type$": "RULE_METADATA_SEARCH_RESPONSE",
 "ruleMetadata": [{ "name": "TESTNAME"}, { "name": "TSTNAME"}, { "name": "TesTNAME"}]
, "totalCount": 1, "problems": []}
"""

TEST_PARSEABLE_ALERT_DETAIL_RESPONSE = """
{
    "type$": "ALERT_DETAILS_RESPONSE",
    "alerts": [
        {
            "type$": "ALERT_DETAILS",
            "observations": [
                {
                    "type$": "OBSERVATION",
                    "id": "example_obsv_id",
                    "observedAt": "2020-01-01T00:00:00.0000000Z",
                    "type": "FedEndpointExfiltration",
                    "data": "{\\"example_key\\":\\"example_string_value\\",\\"example_list\\":[\\"example_list_item_1\\",\\"example_list_item_2\\"]}"
                }
            ]
        }
    ]
}
"""

TEST_NON_PARSEABLE_ALERT_DETAIL_RESPONSE = """
{
    "type$": "ALERT_DETAILS_RESPONSE",
    "alerts": [
        {
            "type$": "ALERT_DETAILS",
            "observations": [
                {
                    "type$": "OBSERVATION",
                    "id": "example_obsv_id",
                    "observedAt": "2020-01-01T00:00:00.0000000Z",
                    "type": "FedEndpointExfiltration",
                    "data": "{\\"invalid_json\\": ][ }"
                }
            ]
        }
    ]
}
"""


@pytest.fixture
def mock_get_all_session(mocker, py42_response):
    py42_response.text = TEST_RESPONSE
    connection = mocker.MagicMock(spec=Connection)
    connection.post.return_value = py42_response
    return connection


class TestAlertService(object):
    @pytest.fixture
    def successful_post(self, mock_connection, successful_response):
        mock_connection.post.return_value = successful_response

    def test_search_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)
        alert_service.search(query)
        post_data = json.loads(mock_connection.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["groupClause"] == "AND"
            and post_data["srtKey"] == "CreatedAt"
            and post_data["srtDirection"] == "desc"
            and post_data["pgSize"] == 500
            and post_data["pgNum"] == 0
            and post_data["groups"][0]["filterClause"] == "AND"
            and post_data["groups"][0]["filters"][0]["operator"] == "IS"
            and post_data["groups"][0]["filters"][0]["term"] == "state"
            and post_data["groups"][0]["filters"][0]["value"] == "OPEN"
        )

    def test_search_posts_to_expected_url(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)
        alert_service.search(query)
        assert mock_connection.post.call_args[0][0] == u"/svc/api/v1/query-alerts"

    def test_get_details_when_not_given_tenant_id_posts_expected_data(
        self, mock_connection, user_context, py42_response
    ):
        py42_response.text = TEST_PARSEABLE_ALERT_DETAIL_RESPONSE
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.get_details(alert_ids)
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    @pytest.mark.parametrize(
        "alert_id", ["ALERT_ID_1", ("ALERT_ID_1",), ["ALERT_ID_1"]]
    )
    def test_get_details_when_given_single_alert_id_posts_expected_data(
        self, mock_connection, user_context, successful_post, py42_response, alert_id
    ):
        py42_response.text = TEST_PARSEABLE_ALERT_DETAIL_RESPONSE
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        alert_service.get_details(alert_id)
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
        )

    def test_get_details_when_given_tenant_id_posts_expected_data(
        self, mock_connection, user_context, successful_post, py42_response
    ):
        py42_response.text = TEST_PARSEABLE_ALERT_DETAIL_RESPONSE
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.get_details(alert_ids)
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_get_details_posts_to_expected_url(
        self, mock_connection, user_context, successful_post, py42_response
    ):
        py42_response.text = TEST_PARSEABLE_ALERT_DETAIL_RESPONSE
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.get_details(alert_ids)
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/query-details"

    def test_get_details_converts_json_observation_strings_to_objects(
        self, mocker, mock_connection, user_context
    ):
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = TEST_PARSEABLE_ALERT_DETAIL_RESPONSE
        py42_response = Py42Response(requests_response)
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        response = alert_service.get_details("alert_id")
        observation_data = response["alerts"][0]["observations"][0]["data"]
        assert observation_data["example_key"] == "example_string_value"
        assert type(observation_data["example_list"]) is list

    def test_get_details_when_observation_data_not_parseable_remains_unchanged(
        self, mocker, mock_connection, user_context
    ):
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = TEST_NON_PARSEABLE_ALERT_DETAIL_RESPONSE
        py42_response = Py42Response(requests_response)
        mock_connection.post.return_value = py42_response
        alert_service = AlertService(mock_connection, user_context)
        response = alert_service.get_details("alert_id")
        observation_data = response["alerts"][0]["observations"][0]["data"]
        expected_observation_data = '{"invalid_json": ][ }'
        assert observation_data == expected_observation_data

    def test_update_state_when_not_given_tenant_id_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.update_state("RESOLVED", alert_ids, "")
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
            and post_data["state"] == "RESOLVED"
            and post_data["note"] == ""
        )

    @pytest.mark.parametrize(
        "alert_id", ["ALERT_ID_1", ("ALERT_ID_1",), ["ALERT_ID_1"]]
    )
    def test_update_state_when_given_single_alert_id_posts_expected_data(
        self, mock_connection, user_context, successful_post, alert_id
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_service.update_state("PENDING", alert_id)
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["state"] == "PENDING"
            and post_data["note"] == ""
        )

    def test_update_state_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.update_state("OPEN", alert_ids, "some-tenant-id")
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
            and post_data["state"] == "OPEN"
            and post_data["note"] == "some-tenant-id"
        )

    def test_update_state_posts_to_expected_url(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.update_state("RESOLVED", alert_ids, "some-tenant-id")
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/update-state"

    def test_update_state_when_note_passed_none_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_service.update_state("RESOLVED", alert_ids, note=None)
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/update-state"
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
            and post_data["state"] == "RESOLVED"
            and post_data["note"] == ""
        )

    def test_get_all_rules_posts_expected_data(self, mock_connection, user_context):
        alert_service = AlertService(mock_connection, user_context)

        for _ in alert_service.get_all_rules(sort_key="key", sort_direction="ASC"):
            break

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            mock_connection.post.call_args[0][0]
            == "/svc/api/v1/rules/query-rule-metadata"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groups"] == []
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 0
            and posted_data["pgSize"] == 500
            and posted_data["srtKey"] == "key"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_all_rules_by_name_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        for _ in alert_service.get_all_rules_by_name(
            "testname", sort_key="key", sort_direction="ASC"
        ):
            break

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        filter_group = posted_data["groups"][0]["filters"][0]

        assert filter_group["term"] == "Name"
        assert filter_group["operator"] == "IS"
        assert filter_group["value"] == "testname"
        assert (
            mock_connection.post.call_args[0][0]
            == "/svc/api/v1/rules/query-rule-metadata"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 0
            and posted_data["pgSize"] == 500
            and posted_data["srtKey"] == "key"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_rule_by_observer_id_posts_expected_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        for _ in alert_service.get_rule_by_observer_id("testid"):
            break

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        filter_group = posted_data["groups"][0]["filters"][0]

        assert filter_group["term"] == "ObserverRuleId"
        assert filter_group["operator"] == "IS"
        assert filter_group["value"] == "testid"
        assert (
            mock_connection.post.call_args[0][0]
            == "/svc/api/v1/rules/query-rule-metadata"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 0
            and posted_data["pgSize"] == 500
            and posted_data["srtKey"] == "CreatedAt"
            and posted_data["srtDirection"] == "DESC"
        )

    def test_get_rules_page_calls_post_with_expected_url_and_data(
        self, mock_connection, user_context, successful_post
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_service.get_rules_page(
            groups=["groups"],
            page_num=1,
            page_size=100,
            sort_key="sort key",
            sort_direction="direction",
        )
        # Note that pgNum is -1 from what is given because of that API
        data = {
            "tenantId": TENANT_ID_FROM_RESPONSE,
            "groups": ["groups"],
            "groupClause": "AND",
            "pgNum": 0,
            "pgSize": 100,
            "srtKey": "sort key",
            "srtDirection": "direction",
        }
        mock_connection.post.assert_called_once_with(
            "/svc/api/v1/rules/query-rule-metadata", json=data
        )

    def test_update_note_calls_post_with_expected_url_and_data(
        self, mock_connection, user_context
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_service.update_note("alert-id", note="Test Note")
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/add-note"
        post_data = mock_connection.post.call_args[1]["json"]
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertId"] == "alert-id"
            and post_data["note"] == "Test Note"
        )

    def test_search_all_pages_posts_expected_data(self, mock_connection, user_context):
        alert_service = AlertService(mock_connection, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)

        for _ in alert_service.search_all_pages(query):
            break

        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/query-alerts"
        post_data = json.loads(mock_connection.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["groupClause"] == "AND"
            and post_data["srtKey"] == "CreatedAt"
            and post_data["srtDirection"] == "desc"
            and post_data["pgSize"] == 500
            and post_data["pgNum"] == 0
            and post_data["groups"][0]["filterClause"] == "AND"
            and post_data["groups"][0]["filters"][0]["operator"] == "IS"
            and post_data["groups"][0]["filters"][0]["term"] == "state"
            and post_data["groups"][0]["filters"][0]["value"] == "OPEN"
        )

    def test_search_posts_expected_data_overwrites_default_option_when_passed_page_num_and_page_size(
        self, mock_connection, user_context
    ):
        alert_service = AlertService(mock_connection, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)

        alert_service.search(query, 10, 20)

        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/query-alerts"
        post_data = json.loads(mock_connection.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["groupClause"] == "AND"
            and post_data["srtKey"] == "CreatedAt"
            and post_data["srtDirection"] == "desc"
            and post_data["pgSize"] == 20
            and post_data["pgNum"] == 9
            and post_data["groups"][0]["filterClause"] == "AND"
            and post_data["groups"][0]["filters"][0]["operator"] == "IS"
            and post_data["groups"][0]["filters"][0]["term"] == "state"
            and post_data["groups"][0]["filters"][0]["value"] == "OPEN"
        )

    def test_get_aggregate_data_calls_post_with_expected_url_and_data(
        self, mock_connection, user_context
    ):
        alert_service = AlertService(mock_connection, user_context)
        alert_service.get_aggregate_data("alert-id")
        assert (
            mock_connection.post.call_args[0][0]
            == "/svc/api/v1/query-details-aggregate"
        )
        post_data = mock_connection.post.call_args[1]["json"]
        assert post_data["alertId"] == "alert-id"
