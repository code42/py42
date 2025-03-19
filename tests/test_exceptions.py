import pytest
from tests.conftest import REQUEST_EXCEPTION_MESSAGE

from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgConflictError
from pycpg.exceptions import PycpgForbiddenError
from pycpg.exceptions import PycpgHTTPError
from pycpg.exceptions import PycpgInternalServerError
from pycpg.exceptions import PycpgNotFoundError
from pycpg.exceptions import PycpgResponseError
from pycpg.exceptions import PycpgTooManyRequestsError
from pycpg.exceptions import PycpgUnauthorizedError
from pycpg.exceptions import raise_pycpg_error


class TestPycpgErrors:
    def test_raise_pycpg_error_raises_bad_request_error(self, error_response):
        error_response.response.status_code = 400
        with pytest.raises(PycpgBadRequestError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_unauthorized_error(self, error_response):
        error_response.response.status_code = 401
        with pytest.raises(PycpgUnauthorizedError, match=REQUEST_EXCEPTION_MESSAGE):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_forbidden_error(self, error_response):
        error_response.response.status_code = 403
        with pytest.raises(PycpgForbiddenError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_not_found_error(self, error_response):
        error_response.response.status_code = 404
        with pytest.raises(PycpgNotFoundError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_conflict_error(self, error_response):
        error_response.response.status_code = 409
        with pytest.raises(PycpgConflictError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_internal_server_error(self, error_response):
        error_response.response.status_code = 500
        with pytest.raises(PycpgInternalServerError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_pycpg_http_error(self, error_response):
        error_response.response.status_code = 600
        with pytest.raises(PycpgHTTPError):
            raise_pycpg_error(error_response)

    def test_raise_pycpg_error_raises_too_many_requests_error(self, error_response):
        error_response.response.status_code = 429
        with pytest.raises(PycpgTooManyRequestsError):
            raise_pycpg_error(error_response)

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 429, 500, 600])
    def test_raise_pycpg_http_error_has_correct_response_type(
        self, error_response, status_code
    ):
        error_response.response.status_code = status_code
        try:
            raise_pycpg_error(error_response)
        except Exception as e:
            assert isinstance(e.response, type(error_response.response))

    def test_raise_pycpg_error_when_has_unexpected_error_returns_api_error_response(
        self, mock_error_response, mocker
    ):
        mock_error_response.response.status_code = 410
        error_message = '{"error": { "message": "error"}}'
        mock_error_response.response.text = error_message
        mock_method = mocker.patch.object(PycpgResponseError, "__init__", autospec=True)
        with pytest.raises(PycpgHTTPError):
            raise_pycpg_error(mock_error_response)
        mock_method.assert_called_with(
            PycpgHTTPError(mock_error_response),
            mock_error_response.response,
            "Failure in HTTP call {}. Response content: {}".format(
                str(mock_error_response), error_message
            ),
        )
