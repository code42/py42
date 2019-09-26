import pytest

from py42._internal.clients.orgs import OrgClient
from py42._internal.session import Py42Session

COMPUTER_URI = "/api/Org"


class TestOrgClient(object):
    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    def test_get_org_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = OrgClient(session, v3_required_session)
        client.get_org_by_id("ORG_ID")
        uri = "{0}/{1}".format(COMPUTER_URI, "ORG_ID")
        session.get.assert_called_once_with(uri)
