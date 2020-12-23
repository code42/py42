import pytest


@pytest.fixture(scope="module")
def rule_id(connection, observer_id):
    response = connection.alerts.rules.get_by_observer_id(observer_id)
    return response["ruleMetadata"][0]["id"]


def test_rules_add_user(connection, new_user, observer_id):
    response = connection.alerts.rules.add_user(observer_id, new_user["userId"])
    assert response.status_code == 200


def test_rules_get_all(connection):
    response_gen = connection.alerts.rules.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_rules_get_by_observer_id(connection, observer_id):
    response = connection.alerts.rules.get_by_observer_id(observer_id)
    assert response.status_code == 200


def test_rules_get_all_by_name(connection):
    response_gen = connection.alerts.rules.get_all_by_name("Test Alerts using CLI")
    for response in response_gen:
        assert response.status_code == 200
        break


def test_rules_get_page(connection):
    response = connection.alerts.rules.get_page()
    assert response.status_code == 200


def test_rules_remove_user(connection, new_user, observer_id):
    response = connection.alerts.rules.remove_user(observer_id, new_user["userId"])
    assert response.status_code == 200


def test_rules_remove_all_users(connection, observer_id):
    response = connection.alerts.rules.remove_all_users(observer_id)
    assert response.status_code == 200


def test_rules_exfiltration_get(connection, rule_id):
    response = connection.alerts.rules.exfiltration.get(rule_id)
    assert response.status_code == 200


def test_rules_cloudshare_get(connection, rule_id):
    response = connection.alerts.rules.cloudshare.get(rule_id)
    assert response.status_code == 200


def test_file_type_mismatch_get(connection, rule_id):
    response = connection.alerts.rules.filetypemismatch.get(rule_id)
    assert response.status_code == 200
