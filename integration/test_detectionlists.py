from datetime import datetime
from datetime import timedelta


new_user = "integration_" + str(int(datetime.now().timestamp())) + "@test.com"
existing_user = "test1-test@test.com"
alias_user = "test_user@test.com"
user_departure_date = datetime.now() + timedelta(days=10)
user_uid = 977335752891390447


def test_get_user_by_id(connection):
    response = connection.detectionlists.get_user_by_id(user_uid)
    assert response.status_code == 200


def test_get_user(connection):
    response = connection.detectionlists.get_user(existing_user)
    assert response.status_code == 200


def test_refresh_user_scim_attributes(connection):
    response = connection.detectionlists.refresh_user_scim_attributes(user_uid)
    assert response.status_code == 200


def test_departing_employee_get_page(connection):
    response = connection.detectionlists.departing_employee.get_page(1)
    assert response.status_code == 200


def test_departing_employee_get(connection):
    response = connection.detectionlists.departing_employee.get(user_uid)
    assert response.status_code == 200


def test_departing_employee_get_all(connection):
    response_gen = connection.detectionlists.departing_employee.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_high_risk_employee_get_all(connection):
    response_gen = connection.detectionlists.high_risk_employee.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_create_user(connection):
    response = connection.detectionlists.create_user(new_user)
    assert response.status_code == 200


def test_add_user_cloud_alias(connection):
    response = connection.detectionlists.add_user_cloud_alias(user_uid, alias_user)
    assert response.status_code == 200


def test_remove_user_cloud_alias(connection):
    response = connection.detectionlists.remove_user_cloud_alias(user_uid, alias_user)
    assert response.status_code == 200


def test_add_user_risk_tags(connection):
    response = connection.detectionlists.add_user_risk_tags(user_uid, "Flight Risk")
    assert response.status_code == 200


def test_remove_user_risk_tags(connection):
    response = connection.detectionlists.remove_user_risk_tags(user_uid, "Flight Risk")
    assert response.status_code == 200


def test_update_user_notes(connection):
    response = connection.detectionlists.update_user_notes(user_uid, "integration test")
    assert response.status_code == 200


def test_departing_employee_add(connection):
    response = connection.detectionlists.departing_employee.add(new_user)
    assert response.status_code == 200


def test_departing_employee_update_departure_date(connection):
    response = connection.detectionlists.departing_employee.update_departure_date(
        user_uid, user_departure_date
    )
    assert response.status_code == 200


def test_departing_employee_remove(connection):
    response = connection.detectionlists.departing_employee.remove(new_user)
    assert response.status_code == 200


def test_departing_employee_set_alerts_enabled(connection):
    response = connection.detectionlists.departing_employee.set_alerts_enabled()
    assert response.status_code == 200


def test_high_risk_employee_add(connection):
    response = connection.detectionlists.high_risk_employee.add(new_user)
    assert response.status_code == 200


def test_high_risk_employee_remove(connection):
    response = connection.detectionlists.high_risk_employee.remove(new_user)
    assert response.status_code == 200


def test_high_risk_employee_get(connection):
    response = connection.detectionlists.high_risk_employee.get(user_uid)
    assert response.status_code == 200


def test_high_risk_employee_get_page(connection):
    response = connection.detectionlists.departing_employee.get_page(1)
    assert response.status_code == 200


def test_high_risk_employee_set_alerts_enabled(connection):
    response = connection.detectionlists.high_risk_employee.set_alerts_enabled()
    assert response.status_code == 200
