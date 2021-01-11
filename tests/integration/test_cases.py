import pytest


@pytest.mark.integration
class TestCases:
    @pytest.fixture(scope="module")
    def case(self, connection, timestamp):
        return connection.cases.create("integration_test_{}".format(timestamp))

    def test_get_all_cases(
        self, connection,
    ):
        page_gen = connection.cases.get_all()
        for response in page_gen:
            assert response.status_code == 200
            break

    def test_get_case_by_case_number(self, connection, case):
        response = connection.cases.get(case["number"])
        assert response.status_code == 200

    def test_update_case(self, connection, case):
        response = connection.cases.update(
            case["number"], findings="integration test case"
        )
        assert response.status_code == 200

    def test_export_summary(self, connection, case):
        response = connection.cases.export_summary(case["number"])
        assert response.status_code == 200

    def test_add_file_event(self, connection, case, event_id):
        response = connection.cases.file_events.add(case["number"], event_id)
        assert response.status_code == 204

    def test_get_file_event(self, connection, case, event_id):
        response = connection.cases.file_events.get(case["number"], event_id)
        assert response.status_code == 200

    def test_delete_file_event(self, connection, case, event_id):
        response = connection.cases.file_events.delete(case["number"], event_id)
        assert response.status_code == 204

    def test_get_all_file_events(self, connection, case):
        response = connection.cases.file_events.get_all(case["number"])
        assert response.status_code == 200
