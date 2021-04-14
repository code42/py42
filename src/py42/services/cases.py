from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseNameExistsError
from py42.exceptions import Py42DescriptionLimitExceededError
from py42.exceptions import Py42InvalidCaseUserError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services import BaseService
from py42.services.util import get_all_pages


class CasesService(BaseService):

    _uri_prefix = u"/api/v1/case"

    def __init__(self, connection):
        super(CasesService, self).__init__(connection)

    def create(
        self, name, subject=None, assignee=None, description=None, findings=None
    ):
        data = {
            u"assignee": assignee,
            u"description": description,
            u"findings": findings,
            u"name": name,
            u"subject": subject,
        }
        try:
            return self._connection.post(self._uri_prefix, json=data)
        except Py42BadRequestError as err:
            _handle_common_invalid_case_parameters_errors(err, name)

    def get_page(
        self,
        page_num,
        name=None,
        status=None,
        created_at=None,
        updated_at=None,
        subject=None,
        assignee=None,
        page_size=None,
        sort_direction=u"asc",
        sort_key=u"number",
        **kwargs
    ):

        page_size = page_size or settings.items_per_page
        params = {
            u"name": name,
            u"subject": subject,
            u"assignee": assignee,
            u"createdAt": created_at,
            u"updatedAt": updated_at,
            u"status": status,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtDir": sort_direction,
            u"srtKey": sort_key,
        }
        params.update(**kwargs)

        return self._connection.get(self._uri_prefix, params=params)

    def get_all(
        self,
        name=None,
        status=None,
        created_at=None,
        updated_at=None,
        subject=None,
        assignee=None,
        page_size=None,
        sort_direction=u"asc",
        sort_key=u"number",
        **kwargs
    ):
        return get_all_pages(
            self.get_page,
            u"cases",
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            assignee=assignee,
            subject=subject,
            page_size=page_size,
            sort_direction=sort_direction,
            sort_key=sort_key,
            **kwargs
        )

    def get(self, case_number):
        return self._connection.get("{}/{}".format(self._uri_prefix, case_number))

    def export_summary(self, case_number):
        uri_prefix = u"{}/{}/{}".format(self._uri_prefix, case_number, u"export")
        return self._connection.get(uri_prefix)

    def update(
        self,
        case_number,
        name=None,
        subject=None,
        assignee=None,
        description=None,
        findings=None,
        status=None,
    ):
        current_case_data = self.get(case_number).data

        data = {
            u"assignee": assignee or current_case_data.get(u"assignee"),
            u"description": description or current_case_data.get(u"description"),
            u"findings": findings or current_case_data.get(u"findings"),
            u"name": name or current_case_data.get(u"name"),
            u"subject": subject or current_case_data.get(u"subject"),
            u"status": status or current_case_data.get("status"),
        }
        try:
            return self._connection.put(
                u"{}/{}".format(self._uri_prefix, case_number), json=data
            )
        except Py42BadRequestError as err:
            if u"NO_EDITS_ONCE_CLOSED" in err.response.text:
                raise Py42UpdateClosedCaseError(err)
            _handle_common_invalid_case_parameters_errors(err, name)


def _handle_common_invalid_case_parameters_errors(base_err, name):
    if u"NAME_EXISTS" in base_err.response.text:
        raise Py42CaseNameExistsError(base_err, name)
    elif u"NO_EDITS_ONCE_CLOSED" in base_err.response.text:
        raise Py42UpdateClosedCaseError(base_err)
    elif u"DESCRIPTION_TOO_LONG" in base_err.response.text:
        raise Py42DescriptionLimitExceededError(base_err)
    elif u"INVALID_USER" in base_err.response.text:
        if u"subject" in base_err.response.text:
            raise Py42InvalidCaseUserError(base_err, u"subject")
        elif u"assignee" in base_err.response.text:
            raise Py42InvalidCaseUserError(base_err, u"assignee")
    raise
