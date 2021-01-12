from collections import namedtuple

Clients = namedtuple(
    u"Clients",
    [
        u"alerts",
        u"archive",
        u"authority",
        u"detectionlists",
        u"securitydata",
        u"auditlogs",
        u"cases",
    ],
)
