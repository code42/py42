from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseNameExistsError
from py42.exceptions import Py42DescriptionLimitExceededError
from py42.exceptions import Py42InvalidCaseUserError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services import BaseService
from py42.services.util import get_all_pages


class CasesService(BaseService):

    _uri_prefix = "/api/v1/case"

    def __init__(self, connection):
        super().__init__(connection)

    def create(
        self, name, subject=None, assignee=None, description=None, findings=None
    ):
        data = {
            "assignee": assignee,
            "description": description,
            "findings": findings,
            "name": name,
            "subject": subject,
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
        sort_direction="asc",
        sort_key="number",
        **kwargs,
    ):

        page_size = page_size or settings.items_per_page
        params = {
            "name": name,
            "subject": subject,
            "assignee": assignee,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "status": status,
            "pgNum": page_num,
            "pgSize": page_size,
            "srtDir": sort_direction,
            "srtKey": sort_key,
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
        sort_direction="asc",
        sort_key="number",
        **kwargs,
    ):
        return get_all_pages(
            self.get_page,
            "cases",
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            assignee=assignee,
            subject=subject,
            page_size=page_size,
            sort_direction=sort_direction,
            sort_key=sort_key,
            **kwargs,
        )

    def get(self, case_number):
        return self._connection.get(f"{self._uri_prefix}/{case_number}")

    def export_summary(self, case_number):
        uri_prefix = f"{self._uri_prefix}/{case_number}/export"
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
            "assignee": assignee or current_case_data.get("assignee"),
            "description": description or current_case_data.get("description"),
            "findings": findings or current_case_data.get("findings"),
            "name": name or current_case_data.get("name"),
            "subject": subject or current_case_data.get("subject"),
            "status": status or current_case_data.get("status"),
        }
        try:
            return self._connection.put(f"{self._uri_prefix}/{case_number}", json=data)
        except Py42BadRequestError as err:
            if "NO_EDITS_ONCE_CLOSED" in err.response.text:
                raise Py42UpdateClosedCaseError(err)
            _handle_common_invalid_case_parameters_errors(err, name)


def _handle_common_invalid_case_parameters_errors(base_err, name):
    if "NAME_EXISTS" in base_err.response.text:
        raise Py42CaseNameExistsError(base_err, name)
    elif "NO_EDITS_ONCE_CLOSED" in base_err.response.text:
        raise Py42UpdateClosedCaseError(base_err)
    elif "DESCRIPTION_TOO_LONG" in base_err.response.text:
        raise Py42DescriptionLimitExceededError(base_err)
    elif "INVALID_USER" in base_err.response.text:
        if "subject" in base_err.response.text:
            raise Py42InvalidCaseUserError(base_err, "subject")
        elif "assignee" in base_err.response.text:
            raise Py42InvalidCaseUserError(base_err, "assignee")
    raise
