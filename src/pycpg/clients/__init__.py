from collections import namedtuple

Clients = namedtuple(
    "Clients",
    [
        "archive",
        "authority",
        "auditlogs",
        "loginconfig",
    ],
)
