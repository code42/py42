from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42ConflictError
from py42.exceptions import Py42DescriptionLimitExceededError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42TrustedActivityConflictError
from py42.exceptions import Py42TrustedActivityIdNotFound
from py42.exceptions import Py42TrustedActivityInvalidCharacterError
from py42.services import BaseService
from py42.services.util import get_all_pages


class TrustedActivitiesService(BaseService):

    _uri_prefix = "/api/v1/trusted-activities"

    def __init__(self, connection):
        super().__init__(connection)

    def get_all(self, type=None, page_size=None, **kwargs):
        return get_all_pages(
            self.get_page, "trustResources", type=type, page_size=page_size, **kwargs
        )

    def get_page(self, page_num, page_size, type, **kwargs):
        page_size = page_size or settings.items_per_page
        params = {
            "type": type,
            "pgNum": page_num,
            "pgSize": page_size,
        }
        params.update(**kwargs)

        return self._connection.get(self._uri_prefix, params=params)

    def create(self, type, value, description=None):
        data = {
            "type": type,
            "value": value,
            "description": description,
        }
        try:
            return self._connection.post(self._uri_prefix, json=data)
        except Py42BadRequestError as err:
            _handle_common_invalid_trust_parameters_errors(err)
        except Py42ConflictError as err:
            raise Py42TrustedActivityConflictError(err, value)

    def get(self, id):
        uri = f"{self._uri_prefix}/{id}"
        try:
            return self._connection.get(uri)
        except Py42NotFoundError as err:
            raise Py42TrustedActivityIdNotFound(err, id)

    def update(self, id, value=None, description=None):
        uri = f"{self._uri_prefix}/{id}"
        current_activity_data = self.get(id).data

        if description is None:
            description = current_activity_data.get("description")

        data = {
            "type": current_activity_data.get("type"),
            "value": value or current_activity_data.get("value"),
            "description": description,
        }
        try:
            return self._connection.put(uri, json=data)
        except Py42BadRequestError as err:
            _handle_common_invalid_trust_parameters_errors(err)
        except Py42NotFoundError as err:
            raise Py42TrustedActivityIdNotFound(err, id)
        except Py42ConflictError as err:
            raise Py42TrustedActivityConflictError(err, value)

    def delete(self, id):
        uri = f"{self._uri_prefix}/{id}"
        try:
            return self._connection.delete(uri)
        except Py42NotFoundError as err:
            raise Py42TrustedActivityIdNotFound(err, id)


def _handle_common_invalid_trust_parameters_errors(base_err):
    if "DESCRIPTION_TOO_LONG" in base_err.response.text:
        raise Py42DescriptionLimitExceededError(base_err)
    elif "INVALID_CHARACTERS_IN_VALUE" in base_err.response.text:
        raise Py42TrustedActivityInvalidCharacterError(base_err)
    raise
