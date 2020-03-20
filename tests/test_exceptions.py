import pytest

from py42.sdk.exceptions import (
    raise_py42_error,
    Py42BadRequestError,
    Py42UnauthorizedError,
    Py42ForbiddenError,
    Py42NotFoundError,
    Py42InternalServerError,
    Py42HTTPError,
)


class TestPy42Errors(object):
    def test_raise_py42_error_raises_bad_request_error(self, error_response):
        error_response.response.status_code = 400
        with pytest.raises(Py42BadRequestError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_unauthorized_error(self, error_response):
        error_response.response.status_code = 401
        with pytest.raises(Py42UnauthorizedError):
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

        error_response.response.status_code = 501
        with pytest.raises(Py42InternalServerError):
            raise_py42_error(error_response)

        error_response.response.status_code = 599
        with pytest.raises(Py42InternalServerError):
            raise_py42_error(error_response)

        error_response.response.status_code = 550
        with pytest.raises(Py42InternalServerError):
            raise_py42_error(error_response)

    def test_raise_py42_error_raises_py42_http_error(self, error_response):
        error_response.response.status_code = 600
        with pytest.raises(Py42HTTPError):
            raise_py42_error(error_response)

        error_response.response.status_code = 999
        with pytest.raises(Py42HTTPError):
            raise_py42_error(error_response)
