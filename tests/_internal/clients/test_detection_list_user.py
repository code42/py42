import json

import pytest
from requests import Response
from requests.exceptions import HTTPError

from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42.clients.users import UserClient
from py42.exceptions import Py42BadRequestError


class TestDetectionListUserClient(object):
    @pytest.fixture
    def mock_user_client(self, mock_session, user_context, py42_response):
        user_client = UserClient(mock_session)
        py42_response.text = '{"username":"username"}'
        mock_session.get.return_value = py42_response
        return user_client

    @pytest.fixture
    def mock_get_by_id_fails(self, mocker, mock_session):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 400
        exception = mocker.MagicMock(spec=HTTPError)
        exception.response = response
        mock_session.post.side_effect = Py42BadRequestError(exception)
        return mock_session

    @pytest.fixture
    def mock_user_client_raises_exception(self, mocker, mock_session, user_context, py42_response):
        user_client = UserClient(mock_session)
        response = mocker.MagicMock(spec=Response)
        response.status_code = 400
        exception = mocker.MagicMock(spec=HTTPError)
        exception.response = response
        mock_session.post.side_effect = Py42BadRequestError(exception)
        return user_client

    def test_create_posts_expected_data(self, mock_session, user_context, mock_user_client):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.create("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/create"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userName"] == "942897397520289999"
            and posted_data["riskFactors"] == []
            and posted_data["cloudUsernames"] == []
            and posted_data["notes"] == ""
        )

    def test_get_posts_expected_data(self, mock_session, user_context, mock_user_client):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.get("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/getbyusername"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["username"] == "942897397520289999"
        )

    def test_get_by_id_posts_expected_data(self, mock_session, user_context, mock_user_client):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.get_by_id("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/getbyid"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_update_notes_posts_expected_data(self, mock_session, user_context, mock_user_client):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.update_notes("942897397520289999", "Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/updatenotes"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["notes"] == "Test"
        )

    @pytest.mark.parametrize("tags", ["test_tag", ("test_tag",), ["test_tag"]])
    def test_add_risk_tag_posts_expected_data(
        self, mock_session, user_context, mock_user_client, tags
    ):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.add_risk_tags("942897397520289999", tags)

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/addriskfactors"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["riskFactors"] == ["test_tag"]
        )

    def test_remove_risk_tag_posts_expected_data(
        self, mock_session, user_context, mock_user_client
    ):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.remove_risk_tags("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/removeriskfactors"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["riskFactors"] == ["Test"]
        )

    def test_add_cloud_alias_posts_expected_data(
        self, mock_session, user_context, mock_user_client
    ):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.add_cloud_alias("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/addcloudusernames"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["cloudUsernames"] == ["Test"]
        )

    def test_remove_cloud_alias_posts_expected_data(
        self, mock_session, user_context, mock_user_client
    ):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.remove_cloud_alias("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/removecloudusernames"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["cloudUsernames"] == ["Test"]
        )

    def test_create_if_not_exists_posts_expected_data_when_user_exists(
        self, mock_session, user_context, mock_user_client
    ):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        assert detection_list_user_client.create_if_not_exists("942897397520289999") is True

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/getbyid"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )
        assert mock_session.post.call_count == 1

    def test_create_if_not_exists_posts_expected_data_when_user_does_not_exist(
        self, mock_get_by_id_fails, user_context, mock_user_client
    ):
        # In this test case we can't verify create successful, hence we verified failure in create
        # because same mock_session instance
        # 'mock_get_by_id_fails' will be called for get & create and its going to return failure.
        # We verified create is being called and two times post method is called, also we
        # verified user_client.get_by_uid is successfully called.
        detection_list_user_client = DetectionListUserClient(
            mock_get_by_id_fails, user_context, mock_user_client
        )
        with pytest.raises(Py42BadRequestError):
            detection_list_user_client.create_if_not_exists("942897397520289999")

        posted_data = json.loads(mock_get_by_id_fails.post.call_args[1]["data"])
        assert mock_get_by_id_fails.post.call_args[0][0] == "/svc/api/v2/user/create"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userName"] == "username"
        )
        assert mock_get_by_id_fails.post.call_count == 2
        assert mock_user_client._session.get.call_count == 1
        assert mock_user_client._session.get.call_args[0][0] == "/api/User/942897397520289999"

    def test_refresh_posts_expected_data(self, mock_session, user_context, mock_user_client):
        detection_list_user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        detection_list_user_client.refresh("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/refresh"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )
