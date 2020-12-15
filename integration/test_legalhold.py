import pytest

SKIP_TEST_MESSAGE = "Changes system state."


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_add_to_matter():
    pass


@pytest.mark.skip("Test failing")
def test_get_all_matter_custodians(connection):
    response_gen = connection.legalhold.get_all_matter_custodians()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_get_matters_page(connection):
    response = connection.legalhold.get_matters_page(1)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_remove_from_matter():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_create_matter():
    pass


def test_get_all_matters(connection):
    response_gen = connection.legalhold.get_all_matters()
    for response in response_gen:
        assert response.status_code == 200
        break


@pytest.mark.skip("Test failing with, Forbidden for url: ..v4/legal-hold-policy/view?l")
def test_get_policy_by_uid(connection):
    response = connection.legalhold.get_policy_by_uid(985033584886712846)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_create_policy():
    pass


@pytest.mark.skip("Test Failing")
def test_get_custodians_page(connection):
    response = connection.legalhold.get_custodians_page(1)
    assert response.status_code == 200


def test_get_policy_list(connection):
    response = connection.legalhold.get_policy_list()
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_deactivate_matter():
    pass


def test_get_matter_by_uid(connection):
    response = connection.legalhold.get_matter_by_uid(985033584886712846)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_reactivate_matter():
    pass
