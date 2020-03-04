import pytest

from py42._internal.login_provider_factories import ArchiveLocatorFactory
from py42._internal.client_factories import (
    AuthorityClientFactory,
    StorageClientFactory,
    MicroserviceClientFactory,
)

_USER_UID = "user-uid"


@pytest.fixture
def login_provider_factory(mocker):
    return mocker.MagicMock(spec=ArchiveLocatorFactory)


@pytest.fixture
def login_providers(mocker):
    return [mocker.MagicMock(), mocker.MagicMock()]


class TestAuthorityClientFactory(object):
    def test_has_set(self, mock_session):
        factory = AuthorityClientFactory(mock_session)


class TestStorageClientFactory(object):
    pass


class TestMicroserviceClientFactory(object):
    pass
