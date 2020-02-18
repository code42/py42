import json

from py42._internal.clients.alerts import AlertClient
from py42.sdk.alert_query import AlertState, AlertQueryFactory


class TestAlertClient(object):
    def test_search_alerts_posts_expected_data(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)
        query_factory = AlertQueryFactory(user_context)
        _filter = AlertState.eq("OPEN")
        query = query_factory.create_query_for_current_tenant(_filter)
        alert_client.search_alerts(query)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and post_data["groupClause"] == "AND"
            and post_data["srtKey"] == "CreatedAt"
            and post_data["srtDir"] == "asc"
            and post_data["pgSize"] == 100
            and post_data["pgNum"] == 0
            and post_data["groups"][0]["filterClause"] == "AND"
            and post_data["groups"][0]["filters"][0]["operator"] == "IS"
            and post_data["groups"][0]["filters"][0]["term"] == "state"
            and post_data["groups"][0]["filters"][0]["value"] == "OPEN"
        )

    def test_search_alerts_posts_to_expected_url(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)
        query_factory = AlertQueryFactory(user_context)
        _filter = AlertState.eq("OPEN")
        query = query_factory.create_query_for_current_tenant(_filter)
        alert_client.search_alerts(query)
        assert mock_session.post.call_args[0][0] == u"/svc/api/v1/query-alerts"

    def test_get_query_details_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_query_details(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_get_query_details_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_query_details(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_get_query_details_posts_to_expected_url(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.get_query_details(alert_ids)
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/query-details"

    def test_resolve_alert_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve_alert(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_resolve_alert_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve_alert(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_resolve_alert_posts_to_expected_url(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.resolve_alert(alert_ids, "some-tenant-id")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/resolve-alert"

    def test_reopen_alert_when_not_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen_alert(alert_ids)
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_reopen_alert_when_given_tenant_id_posts_expected_data(
        self, mock_session, user_context
    ):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen_alert(alert_ids, "some-tenant-id")
        post_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            post_data["tenantId"] == "some-tenant-id"
            and post_data["alertIds"][0] == "ALERT_ID_1"
            and post_data["alertIds"][1] == "ALERT_ID_2"
        )

    def test_reopen_alert_posts_to_expected_url(self, mock_session, user_context):
        alert_client = AlertClient(mock_session, user_context)
        alert_ids = ["ALERT_ID_1", "ALERT_ID_2"]
        alert_client.reopen_alert(alert_ids, "some-tenant-id")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/reopen-alert"
