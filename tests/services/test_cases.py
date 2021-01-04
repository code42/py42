from py42.services.cases import CasesService

DUMMY_GET_ALL_TEST_RESPONSE = {
    "cases": [
        {
            "assignee": "string",
            "assigneeUsername": "string",
            "createdAt": "2021-01-04T08:09:58.832Z",
            "createdByUserUid": "string",
            "createdByUsername": "string",
            "lastModifiedByUserUid": "string",
            "lastModifiedByUsername": "string",
            "name": "string",
            "number": 0,
            "status": "OPEN",
            "subject": "string",
            "subjectUsername": "string",
            "updatedAt": "2021-01-04T08:09:58.832Z",
        }
    ],
    "totalCount": 0,
}


class TestCasesService:
    def test_create_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.create(
            u"name", u"subject", u"user uid", u"description", u"findings"
        )
        assert mock_connection.post.call_args[0][0] == u"/api/v1/case"
        print(mock_connection.post.call_args[0][1])
        post_data = mock_connection.post.call_args[0][1]
        assert (
            post_data["name"] == u"name"
            and post_data["subject"] == u"subject"
            and post_data["assignee"] == u"user uid"
            and post_data["description"] == u"description"
            and post_data["findings"] == u"findings"
        )

    def test_get_all_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        mock_connection.get.side_effect = [
            DUMMY_GET_ALL_TEST_RESPONSE,
            DUMMY_GET_ALL_TEST_RESPONSE,
        ]
        for _ in cases_service.get_all():
            continue

        mock_connection.get.call_count == 2
        assert (
            mock_connection.get.call_args[0][0]
            == u"/api/v1/case?pgNum=1&pgSize=500&srtDir=asc&srtKey=number"
        )

    def test_export_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.export_summary(123456)
        assert mock_connection.get.call_args[0][0] == u"/api/v1/case/123456/export"

    def test_get_case_by_case_number_called_with_expected_url_and_params(
        self, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        cases_service.get_case(123456)
        assert mock_connection.get.call_args[0][0] == u"/api/v1/case/123456"

    def test_update_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.update(123456, findings=u"x")
        assert mock_connection.put.call_args[0][0] == u"/api/v1/case/123456"
        post_data = mock_connection.put.call_args[0][1]
        assert (
            post_data["name"] == u""
            and post_data["subject"] == u""
            and post_data["assignee"] == u""
            and post_data["description"] == u""
            and post_data["findings"] == u"x"
        )