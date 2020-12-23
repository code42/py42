from datetime import datetime
from datetime import timedelta

import pytest

alias_user = "test_user@test.com"
user_departure_date = datetime.now() + timedelta(days=10)


@pytest.mark.integration
class TestDetectionLists:
    def test_create_user(self, connection, new_user):
        response = connection.detectionlists.create_user(new_user["username"])
        assert response.status_code == 200

    def test_get_user_by_id(self, connection, new_user):
        response = connection.detectionlists.get_user_by_id(new_user["userUid"])
        assert response.status_code == 200

    def test_get_user(self, connection, new_user):
        response = connection.detectionlists.get_user(new_user["username"])
        assert response.status_code == 200

    def test_refresh_user_scim_attributes(self, connection, new_user):
        response = connection.detectionlists.refresh_user_scim_attributes(
            new_user["userUid"]
        )
        assert response.status_code == 200

    def test_departing_employee_get_page(self, connection):
        response = connection.detectionlists.departing_employee.get_page(1)
        assert response.status_code == 200

    def test_departing_employee_get_all(self, connection):
        response_gen = connection.detectionlists.departing_employee.get_all()
        for response in response_gen:
            assert response.status_code == 200
            break

    def test_high_risk_employee_get_all(self, connection):
        response_gen = connection.detectionlists.high_risk_employee.get_all()
        for response in response_gen:
            assert response.status_code == 200
            break

    def test_add_user_cloud_alias(self, connection, new_user):
        response = connection.detectionlists.add_user_cloud_alias(
            new_user["userUid"], alias_user
        )
        assert response.status_code == 200

    def test_remove_user_cloud_alias(self, connection, new_user):
        response = connection.detectionlists.remove_user_cloud_alias(
            new_user["userUid"], alias_user
        )
        assert response.status_code == 200

    def test_departing_employee_add(self, connection, new_user):
        response = connection.detectionlists.departing_employee.add(
            new_user['userUid']
        )
        assert response.status_code == 200

    def test_departing_employee_get(self, connection, new_user):
        response = connection.detectionlists.departing_employee.get(new_user["userUid"])
        assert response.status_code == 200

    def test_departing_employee_update_departure_date(self, connection, new_user):
        response = connection.detectionlists.departing_employee.update_departure_date(
            new_user["userUid"], user_departure_date
        )
        assert response.status_code == 200

    def test_add_user_risk_tags(self, connection, new_user):
        response = connection.detectionlists.add_user_risk_tags(
            new_user["userUid"], "Flight_Risk"
        )
        assert response.status_code == 200

    def test_remove_user_risk_tags(self, connection, new_user):
        response = connection.detectionlists.remove_user_risk_tags(
            new_user["userUid"], "Flight_Risk"
        )
        assert response.status_code == 200

    def test_update_user_notes(self, connection, new_user):
        response = connection.detectionlists.update_user_notes(
            new_user["userUid"], "integration test"
        )
        assert response.status_code == 200

    def test_departing_employee_remove(self, connection, new_user):
        response = connection.detectionlists.departing_employee.remove(
            new_user["userUid"]
        )
        assert response.status_code == 200

    def test_departing_employee_set_alerts_enabled(self, connection):
        response = connection.detectionlists.departing_employee.set_alerts_enabled()
        assert response.status_code == 200

    def test_high_risk_employee_add(self, connection, new_user):
        response = connection.detectionlists.high_risk_employee.add(
            new_user["userUid"]
        )
        assert response.status_code == 200

    def test_high_risk_employee_get(self, connection, new_user):
        response = connection.detectionlists.high_risk_employee.get(new_user["userUid"])
        assert response.status_code == 200

    def test_high_risk_employee_remove(self, connection, new_user):
        response = connection.detectionlists.high_risk_employee.remove(
            new_user["userUid"]
        )
        assert response.status_code == 200

    def test_high_risk_employee_get_page(self, connection):
        response = connection.detectionlists.departing_employee.get_page(1)
        assert response.status_code == 200

    def test_high_risk_employee_set_alerts_enabled(self, connection):
        response = connection.detectionlists.high_risk_employee.set_alerts_enabled()
        assert response.status_code == 200
