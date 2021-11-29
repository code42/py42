import pytest
from tests.integration.conftest import assert_successful_response


@pytest.fixture(scope="module")
def policy(api_client_connection, timestamp):
    policy_name = f"integration test policy {timestamp}"
    response = api_client_connection.legalhold.create_policy(policy_name)
    assert_successful_response(response)
    return response["legalHoldPolicyUid"]


@pytest.fixture(scope="module")
def matter(api_client_connection, policy, timestamp):
    matter_name = f"integration test matter {timestamp}"
    response = api_client_connection.legalhold.create_matter(matter_name, policy)
    assert_successful_response(response)
    return response["legalHoldUid"]

@pytest.fixture
def membership(api_client_connection, matter, new_user):
    response = api_client_connection.legalhold.add_to_matter(
        new_user["userUid"], matter
    )
    assert_successful_response(response)
    return response["legalHoldMembershipUid"]

@pytest.mark.integration
class TestLegalHoldApiClient:
    # test a GET and POST from each path

    # legal hold membership endpoints
    def test_get_all_matter_custodians(self, connection, policy, matter):
        response_gen = connection.legalhold.get_all_matter_custodians(policy, matter)
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_remove_from_matter(self, api_client_connection, membership):
        response = api_client_connection.legalhold.remove_from_matter(membership)
        assert_successful_response(response)

    # legal hold policy endpoints
    def test_get_policy_by_uid(self, api_client_connection, policy):
        response = api_client_connection.legalhold.get_policy_by_uid(policy)
        assert_successful_response(response)

    def test_get_policy_list(self, api_client_connection):
        response = api_client_connection.legalhold.get_policy_list()
        assert_successful_response(response)

    # legal hold matter endpoints
    def test_get_matter_by_uid(self, api_client_connection, matter):
        response = api_client_connection.legalhold.get_matter_by_uid(matter)
        assert_successful_response(response)

    def test_get_all_matters(self, api_client_connection):
        response_gen = api_client_connection.legalhold.get_all_matters()
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_deactivate_matter(self, api_client_connection, matter):
        response = api_client_connection.legalhold.deactivate_matter(matter)
        assert_successful_response(response)

    def test_reactivate_matter(self, api_client_connection, matter):
        response = api_client_connection.legalhold.reactivate_matter(matter)
        assert_successful_response(response)
