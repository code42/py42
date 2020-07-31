from py42.exceptions import Py42UserAlreadyAddedError

_PAGE_SIZE = 100


def handle_user_already_added_error(bad_request_err, username_tried_adding, list_name):
    if u"User already on list" in bad_request_err.response.text:
        raise Py42UserAlreadyAddedError(username_tried_adding, list_name)
    return False
