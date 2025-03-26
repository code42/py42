from collections import namedtuple

Clients = namedtuple(
    "Clients",
    [
        "alerts",
        "archive",
        "authority",
        "securitydata",
        "auditlogs",
        "cases",
        "loginconfig",
        "trustedactivities",
        "userriskprofile",
        "watchlists",
    ],
)
