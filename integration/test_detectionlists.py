import pytest

SKIP_TEST_MESSAGE = "Changes system state."


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_add_user_cloud_alias():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_remove_user_risk_tags():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_add_user_risk_tags():
    pass


def test_get_user(connection):
    response = connection.detectionlists.get_user("test1-test@test.com")
    assert response.status_code == 200


def test_refresh_user_scim_attributes(connection):
    response = connection.detectionlists.refresh_user_scim_attributes(
        977335752891390447
    )
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_update_user_notes():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_create_user():
    pass


def test_get_user_by_id(connection):
    response = connection.detectionlists.get_user_by_id(977335752891390447)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_remove_user_cloud_alias():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_departing_employee_add():
    pass


def test_departing_employee_get_page(connection):
    response = connection.detectionlists.departing_employee.get_page(1)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_departing_employee_update_departure_date():
    pass


def test_departing_employee_get(connection):
    response = connection.detectionlists.departing_employee.get(977335752891390447)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_departing_employee_remove():
    pass


def test_departing_employee_get_all(connection):
    response_gen = connection.detectionlists.departing_employee.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_departing_employee_set_alerts_enabled():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_high_risk_employee_add():
    pass


def test_high_risk_employee_get_all(connection):
    response_gen = connection.detectionlists.high_risk_employee.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_high_risk_employee_remove():
    pass


def test_high_risk_employee_get(connection):
    response = connection.detectionlists.high_risk_employee.get(977335752891390447)
    assert response.status_code == 200


def test_high_risk_employee_get_page(connection):
    response = connection.detectionlists.departing_employee.get_page(1)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_high_risk_employee_set_alerts_enabled():
    pass
