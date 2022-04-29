from collections import namedtuple

Clients = namedtuple(
    "Clients",
    [
        "alerts",
        "archive",
        "authority",
        "detectionlists",
        "securitydata",
        "auditlogs",
        "cases",
        "loginconfig",
        "trustedactivities",
        "userriskprofile",
        "watchlists",
    ],
)
