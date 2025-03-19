from collections import namedtuple

from pycpg.exceptions import PycpgActiveLegalHoldError


def handle_active_legal_hold_error(bad_request_err, resource, resource_id):
    if "ACTIVE_LEGAL_HOLD" in bad_request_err.response.text:
        raise PycpgActiveLegalHoldError(bad_request_err, resource, resource_id)


class BaseService:

    __slots__ = ["_connection"]

    def __init__(self, connection):
        self._connection = connection


Services = namedtuple(
    "Services",
    [
        "administration",
        "archive",
        "devices",
        "legalhold",
        "orgs",
        "users",
        "auditlogs",
    ],
)
