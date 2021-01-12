from collections import namedtuple

from py42.exceptions import Py42ActiveLegalHoldError


def handle_active_legal_hold_error(bad_request_err, resource, resource_id):
    if u"ACTIVE_LEGAL_HOLD" in bad_request_err.response.text:
        raise Py42ActiveLegalHoldError(bad_request_err, resource, resource_id)


class BaseService(object):

    __slots__ = ["_connection"]

    def __init__(self, connection):
        self._connection = connection


Services = namedtuple(
    u"Services",
    [
        u"administration",
        u"archive",
        u"devices",
        u"legalhold",
        u"orgs",
        u"securitydata",
        u"users",
        u"alertrules",
        u"alerts",
        u"fileevents",
        u"savedsearch",
        u"preservationdata",
        u"departingemployee",
        u"highriskemployee",
        u"userprofile",
        u"auditlogs",
        u"cases",
        u"casesfileevents",
    ],
)
