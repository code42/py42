from datetime import datetime

import pytest

timestamp = str(int(datetime.utcnow().timestamp()))
matter_name = "integration test matter {}".format(timestamp)
policy_name = "integration test policy {}".format(timestamp)


@pytest.fixture(scope="module")
def policy(connection):
    response = connection.legalhold.create_policy(policy_name)
    assert response.status_code == 200
    return response["legalHoldPolicyUid"]


@pytest.fixture(scope="module")
def matter(connection, policy):
    response = connection.legalhold.create_matter(matter_name, policy)
    assert response.status_code == 201
    return response["legalHoldUid"]


@pytest.fixture
def membership(connection, matter, new_user):
    response = connection.legalhold.add_to_matter(new_user["userUid"], matter)
    assert response.status_code == 201
    return response["legalHoldMembershipUid"]


@pytest.mark.integration
class TestLegalhold:
    def test_get_policy_by_uid(self, connection, policy):
        response = connection.legalhold.get_policy_by_uid(policy)
        assert response.status_code == 200

    def test_get_policy_list(self, connection):
        response = connection.legalhold.get_policy_list()
        assert response.status_code == 200

    def test_get_all_matter_custodians(self, connection, policy, matter):
        response_gen = connection.legalhold.get_all_matter_custodians(policy, matter)
        for response in response_gen:
            assert response.status_code == 200
            break

    def test_get_matters_page(self, connection):
        response = connection.legalhold.get_matters_page(1)
        assert response.status_code == 200

    def test_remove_from_matter(self, connection, membership):
        response = connection.legalhold.remove_from_matter(membership)
        assert response.status_code == 204

    def test_get_all_matters(self, connection):
        response_gen = connection.legalhold.get_all_matters()
        for response in response_gen:
            assert response.status_code == 200
            break

    def test_get_custodians_page(self, connection, membership):
        response = connection.legalhold.get_custodians_page(
            1, legal_hold_membership_uid=membership
        )
        assert response.status_code == 200

    def test_deactivate_matter(self, connection, matter):
        response = connection.legalhold.deactivate_matter(matter)
        assert response.status_code == 204

    def test_get_matter_by_uid(self, connection, matter):
        response = connection.legalhold.get_matter_by_uid(matter)
        assert response.status_code == 200

    def test_reactivate_matter(self, connection, matter):
        response = connection.legalhold.reactivate_matter(matter)
        assert response.status_code == 201
