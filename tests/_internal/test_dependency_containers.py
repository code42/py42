from requests import Response

from py42._internal.dependency_containers import AuthorityDependencies
from py42._internal.session import Py42Session
from py42._internal.session_factory import SessionFactory


class TestAuthorityDependencies(object):
    def test_constructs_successfully(self, mocker):
        session_factory = mocker.MagicMock(spec=SessionFactory)

        response = mocker.MagicMock(spec=Response)
        response.status_code = 200

        v3_session = mocker.MagicMock(spec=Py42Session)
        v3_session.get.return_value = response
        session_factory.create_jwt_session.return_value = v3_session

        v1_session = mocker.MagicMock(spec=Py42Session)
        v1_session.get.return_value = response
        session_factory.create_v1_session.return_value = v1_session

        root_session = mocker.MagicMock(spec=Py42Session)

        authority_dependencies = AuthorityDependencies(session_factory, root_session)
        assert authority_dependencies is not None
