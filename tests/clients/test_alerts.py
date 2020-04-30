import json
import pytest

from py42._internal.session import Py42Session
from py42._internal.clients.alerts import AlertClient
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import AlertState
from tests.conftest import TENANT_ID_FROM_RESPONSE


TEST_RESPONSE = """
{"type$": "RULE_METADATA_SEARCH_RESPONSE",
 "ruleMetadata": [{ "name": "TESTNAME"}, { "name": "TSTNAME"}, { "name": "TesTNAME"}]
, "totalCount": 1, "problems": []}
"""


@pytest.fixture
def mock_get_all_session(mocker, py42_response):
    py42_response.text = TEST_RESPONSE
    session = mocker.MagicMock(spec=Py42Session)
    session.post.return_value = py42_response
    return session


class TestAlertClient(object):
    @pytest.fixture
    def successful_post(self, mock_session, successful_response):
        mock_session.post.return_value = successful_response

    def test_search_posts_expected_data(self, mock_session, user_context, successful_post):
        alert_client = AlertClient(mock_session, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)
        alert_client.search(query)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["groupClause"] == "AND"
            and post_data["srtKey"] == "CreatedAt"
            and post_data["srtDirection"] == "desc"
            and post_data["pgSize"] == 10000
            and post_data["pgNum"] == 0
            and post_data["groups"][0]["filterClause"] == "AND"
            and post_data["groups"][0]["filters"][0]["operator"] == "IS"
            and post_data["groups"][0]["filters"][0]["term"] == "state"
            and post_data["groups"][0]["filters"][0]["value"] == "OPEN"
        )

    def test_search_posts_to_expected_url(self, mock_session, user_context, successful_post):
        alert_client = AlertClient(mock_session, user_context)
        _filter = AlertState.eq("OPEN")
        query = AlertQuery(_filter)
        alert_client.search(query)
        assert mock_session.post.call_args[0][0] == u"/svc/api/v1/query-alerts"

    def test_get_details_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_response
    ):
        mock_session.post.return_value = successful_response
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_details(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_get_details_when_given_single_alert_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_client.get_details("ALERT_ID_1")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
        )

    def test_get_details_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_details(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_get_details_posts_to_expected_url(self, mock_session, user_context, successful_post):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_details(alert_ids)
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/query-details"

    def test_resolve_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_resolve_when_given_single_alert_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_client.resolve("ALERT_ID_1")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
        )

    def test_resolve_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_resolve_posts_to_expected_url(self, mock_session, user_context, successful_post):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve(alert_ids, "some-tenant-id")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/resolve-alert"

    def test_reopen_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_reopen_when_given_single_alert_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_client.reopen("ALERT_ID_1")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and post_data["alertIds"][0] == "ALERT_ID_1"
        )

    def test_reopen_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context, successful_post
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_reopen_posts_to_expected_url(self, mock_session, user_context, successful_post):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen(alert_ids, "some-tenant-id")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/reopen-alert"

    def test_get_all_posts_expected_data(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)

        for _ in alert_client.get_all_rules(sort_key="key", sort_direction="ASC"):
            break

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/rules/query-rule-metadata"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groups"] == []
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 0
            and posted_data["pgSize"] == 1000
            and posted_data["srtKey"] == "key"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_by_name_filters_correct_record(self, mock_get_all_session, user_context):
        alert_client = AlertClient(mock_get_all_session, user_context)
        rule = alert_client.get_rules_by_name(u"TESTNAME")
        assert len(rule) == 2

    def test_get_by_name_filters_correct_record_case_insenstive_search(
        self, mock_get_all_session, user_context
    ):
        alert_client = AlertClient(mock_get_all_session, user_context)
        rule = alert_client.get_rules_by_name(u"TestName")
        assert len(rule) == 2

    def test_get_by_name_raises_exception_when_name_does_not_match(
        self, mock_get_all_session, user_context
    ):
        alert_client = AlertClient(mock_get_all_session, user_context)
        rule = alert_client.get_rules_by_name(u"TESTNAME2")
        assert len(rule) == 0
