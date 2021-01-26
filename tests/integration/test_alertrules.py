import pytest
from tests.integration.conftest import assert_successful_response


@pytest.fixture(scope="module")
def rule_id(connection, observer_id):
    response = connection.alerts.rules.get_by_observer_id(observer_id)
    return response["ruleMetadata"][0]["id"]


@pytest.mark.integration
class TestAlertRules:
    def test_rules_add_user(self, connection, new_user, observer_id):
        response = connection.alerts.rules.add_user(observer_id, new_user["userUid"])
        assert_successful_response(response)

    def test_rules_get_all(self, connection):
        response_gen = connection.alerts.rules.get_all()
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_rules_get_by_observer_id(self, connection, observer_id):
        response = connection.alerts.rules.get_by_observer_id(observer_id)
        assert_successful_response(response)

    def test_rules_get_all_by_name(self, connection):
        response_gen = connection.alerts.rules.get_all_by_name("Test Alerts using CLI")
        for response in response_gen:
            assert_successful_response(response)
            break

    def test_rules_get_page(self, connection):
        response = connection.alerts.rules.get_page()
        assert_successful_response(response)

    def test_rules_remove_user(self, connection, new_user, observer_id):
        response = connection.alerts.rules.remove_user(observer_id, new_user["userId"])
        assert_successful_response(response)

    def test_rules_remove_all_users(self, connection, observer_id):
        response = connection.alerts.rules.remove_all_users(observer_id)
        assert_successful_response(response)

    def test_rules_exfiltration_get(self, connection, rule_id):
        response = connection.alerts.rules.exfiltration.get(rule_id)
        assert_successful_response(response)

    def test_rules_cloudshare_get(self, connection, rule_id):
        response = connection.alerts.rules.cloudshare.get(rule_id)
        assert_successful_response(response)

    def test_file_type_mismatch_get(self, connection, rule_id):
        response = connection.alerts.rules.filetypemismatch.get(rule_id)
        assert_successful_response(response)
