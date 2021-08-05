import pytest
from tests.integration.conftest import assert_successful_response


@pytest.fixture(scope="module")
def policy(connection, timestamp):
    policy_name = f"integration test policy {timestamp}"
    response = connection.legalhold.create_policy(policy_name)
    assert_successful_response(response)
    return response["legalHoldPolicyUid"]


@pytest.fixture(scope="module")
def matter(connection, policy, timestamp):
    matter_name = f"integration test matter {timestamp}"
    response = connection.legalhold.create_matter(matter_name, policy)
    assert_successful_response(response)
    return response["legalHoldUid"]


@pytest.fixture
def membership(connection, matter, new_user):
    response = connection.legalhold.add_to_matter(new_user["userUid"], matter)
    assert_successful_response(response)
    return response["legalHoldMembershipUid"]


@pytest.mark.integration
class TestLegalhold:
    def test_get_policy_by_uid(self, connection, policy):
        response = connection.legalhold.get_policy_by_uid(policy)
        assert_successful_response(response)

    def test_get_policy_list(self, connection):
        response = connection.legalhold.get_policy_list()
        assert_successful_response(response)

    def test_get_all_matter_custodians(self, connection, policy, matter):
        response_gen = connection.legalhold.get_all_matter_custodians(policy, matter)
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_get_matters_page(self, connection):
        response = connection.legalhold.get_matters_page(1)
        assert_successful_response(response)

    def test_remove_from_matter(self, connection, membership):
        response = connection.legalhold.remove_from_matter(membership)
        assert_successful_response(response)

    def test_get_all_matters(self, connection):
        response_gen = connection.legalhold.get_all_matters()
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_get_custodians_page(self, connection, membership):
        response = connection.legalhold.get_custodians_page(
            1, legal_hold_membership_uid=membership
        )
        assert_successful_response(response)

    def test_deactivate_matter(self, connection, matter):
        response = connection.legalhold.deactivate_matter(matter)
        assert_successful_response(response)

    def test_get_matter_by_uid(self, connection, matter):
        response = connection.legalhold.get_matter_by_uid(matter)
        assert_successful_response(response)

    def test_reactivate_matter(self, connection, matter):
        response = connection.legalhold.reactivate_matter(matter)
        assert_successful_response(response)
