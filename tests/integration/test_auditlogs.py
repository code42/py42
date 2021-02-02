import pytest
from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestAuditLogs:
    def test_get_page(self, connection):
        response = connection.auditlogs.get_page()
        assert_successful_response(response)

    def test_get_all(self, connection):
        page_gen = connection.auditlogs.get_all()
        for response in page_gen:
            assert_successful_response(response)
            break
