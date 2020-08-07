from py42.exceptions import Py42UserAlreadyAddedError

_PAGE_SIZE = 100


def handle_user_already_added_error(bad_request_err, username_tried_adding, list_name):
    if u"User already on list" in bad_request_err.response.text:
        raise Py42UserAlreadyAddedError(
            bad_request_err, username_tried_adding, list_name
        )


class _DetectionListFilters(object):
    OPEN = u"OPEN"
    EXFILTRATION_30_DAYS = u"EXFILTRATION_30_DAYS"
    EXFILTRATION_24_HOURS = u"EXFILTRATION_24_HOURS"
