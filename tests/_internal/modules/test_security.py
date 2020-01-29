import pytest

from py42._internal.client_factories import FileEventClientFactory, StorageClientFactory
from py42._internal.clients.fileevent.file_event import FileEventClient
from py42._internal.clients.security import SecurityClient
from py42._internal.modules.security import SecurityModule

RAW_QUERY = "RAW JSON QUERY"


class TestSecurityModule(object):
    @pytest.fixture
    def security_client(self, mocker):
        return mocker.MagicMock(spec=SecurityClient)

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
