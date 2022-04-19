from collections import namedtuple

from py42.exceptions import Py42ActiveLegalHoldError


def handle_active_legal_hold_error(bad_request_err, resource, resource_id):
    if "ACTIVE_LEGAL_HOLD" in bad_request_err.response.text:
        raise Py42ActiveLegalHoldError(bad_request_err, resource, resource_id)


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
        "alertrules",
        "alerts",
        "fileevents",
        "savedsearch",
        "preservationdata",
        "departingemployee",
        "highriskemployee",
        "userprofile",
        "auditlogs",
        "cases",
        "casesfileevents",
        "trustedactivities",
        "userriskprofile",
        "watchlists",
    ],
)
