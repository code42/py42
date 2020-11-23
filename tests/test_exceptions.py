import pytest

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42ForbiddenError
from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42MFARequiredError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42TooManyRequestsError
from py42.exceptions import Py42UnauthorizedError
from py42.exceptions import raise_py42_error


class TestPy42Errors(object):
    def test_raise_py42_error_raises_bad_request_error(self, error_response):
        error_response.response.status_code = 400
        with pytest.raises(Py42BadRequestError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_unauthorized_error(self, error_response):
        error_response.response.status_code = 401
        with pytest.raises(Py42UnauthorizedError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_MFA_required_error(self, error_response):
        error_response.response.status_code = 401
        error_response.response.text = (
            '{"error":[{"primaryErrorKey":"TIME_BASED_ONE_TIME_PASSWORD_REQUIRED"}]}'
        )
        with pytest.raises(Py42MFARequiredError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_forbidden_error(self, error_response):
        error_response.response.status_code = 403
        with pytest.raises(Py42ForbiddenError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_not_found_error(self, error_response):
        error_response.response.status_code = 404
        with pytest.raises(Py42NotFoundError):
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

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500, 600])
    def test_raise_py42_http_error_has_correct_response_type(
        self, error_response, status_code
    ):
        error_response.response.status_code = status_code
        try:
            raise_py42_error(error_response)
        except Exception as e:
            assert isinstance(e.response, type(error_response.response))
