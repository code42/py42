import pytest

from py42._internal.client_factories import ArchiveLocatorFactory

_USER_UID = "user-uid"


@pytest.fixture
def login_provider_factory(mocker):
    return mocker.MagicMock(spec=ArchiveLocatorFactory)


@pytest.fixture
def login_providers(mocker):
    return [mocker.MagicMock(), mocker.MagicMock()]
