import pytest
from tests.conftest import REQUEST_EXCEPTION_MESSAGE

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42ConflictError
from py42.exceptions import Py42ForbiddenError
from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42ResponseError
from py42.exceptions import Py42TooManyRequestsError
from py42.exceptions import Py42UnauthorizedError
from py42.exceptions import raise_py42_error


class TestPy42Errors:
    def test_raise_py42_error_raises_bad_request_error(self, error_response):
        error_response.response.status_code = 400
        with pytest.raises(Py42BadRequestError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_unauthorized_error(self, error_response):
        error_response.response.status_code = 401
        with pytest.raises(Py42UnauthorizedError, match=REQUEST_EXCEPTION_MESSAGE):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_forbidden_error(self, error_response):
        error_response.response.status_code = 403
        with pytest.raises(Py42ForbiddenError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_not_found_error(self, error_response):
        error_response.response.status_code = 404
        with pytest.raises(Py42NotFoundError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_conflict_error(self, error_response):
        error_response.response.status_code = 409
        with pytest.raises(Py42ConflictError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_internal_server_error(self, error_response):
        error_response.response.status_code = 500
        with pytest.raises(Py42InternalServerError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_py42_http_error(self, error_response):
        error_response.response.status_code = 600
        with pytest.raises(Py42HTTPError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_too_many_requests_error(self, error_response):
        error_response.response.status_code = 429
        with pytest.raises(Py42TooManyRequestsError):
            raise_py42_error(error_response)

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 409, 429, 500, 600])
    def test_raise_py42_http_error_has_correct_response_type(
        self, error_response, status_code
    ):
        error_response.response.status_code = status_code
        try:
            raise_py42_error(error_response)
        except Exception as e:
            assert isinstance(e.response, type(error_response.response))

    def test_raise_py42_error_when_has_unexpected_error_returns_api_error_response(
        self, mock_error_response, mocker
    ):
        mock_error_response.response.status_code = 410
        error_message = '{"error": { "message": "error"}}'
        mock_error_response.response.text = error_message
        mock_method = mocker.patch.object(Py42ResponseError, "__init__", autospec=True)
        with pytest.raises(Py42HTTPError):
            raise_py42_error(mock_error_response)
        mock_method.assert_called_with(
            Py42HTTPError(mock_error_response),
            mock_error_response.response,
            "Failure in HTTP call {}. Response content: {}".format(
                str(mock_error_response), error_message
            ),
        )
