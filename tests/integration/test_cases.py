import pytest


@pytest.mark.integration
class TestCases:

    def test_create_case(connection):
        response = connection.cases.create_case()
        assert response.status_code == 200

    def test_get_all_cases(connection):
        response = connection.cases.get_all()
        assert response.status_code == 200

    def test_get_case_by_case_number(connection):
        response = connection.cases.get_case_by_case_number()
        assert response.status_code == 200

    def test_update_case(connection):
        response = connection.cases.update()
        assert response.status_code == 200

    def test_export_summary(connection):
        response = connection.cases.export_summary()
        assert response.status_code == 200

    def test_add_file_event(connection):
        response = connection.cases.file_events.add_event()
        assert response.status_code == 200

    def test_delete_file_event(connection):
        response = connection.cases.file_events.delete_event()
        assert response.status_code == 200

    def test_get_file_event(connection):
        response = connection.cases.file_events.get_event()
        assert response.status_code == 200

    def test_get_all_file_events(connection):
        response = connection.cases.file_events.get_all_events()
        assert response.status_code == 200
