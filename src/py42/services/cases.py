from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.settings import items_per_page


class CasesService(BaseService):
    """`Rest documentation <https://default-cases.core-int.cloud.code42.com/swagger-ui.html#/Cases>`__ ."""

    _uri_prefix = u"/api/v1/case"

    def __init__(self, connection):
        super(CasesService, self).__init__(connection)

    def create(
        self, name, subject=None, assignee=None, description=None, findings=None
    ):
        """Creates a new case.

        Args:
            name (str): Name of the case.
            subject (str, optional): User UID of the subject of the case.
            assignee (str, optional): User UID of the assignee.
            description (str, optional): Description of the case
            findings (str, optional): Notes on the case.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {
            u"assignee": assignee,
            u"description": description,
            u"findings": findings,
            u"name": name,
            u"subject": subject,
        }
        return self._connection.post(self._uri_prefix, data)

    def get_page(
        self,
        name=None,
        status=None,
        created_at=None,
        updated_at=None,
        subject=None,
        assignee=None,
        page_num=1,
        page_size=items_per_page,
        sort_direction=u"asc",
        sort_key=u"number",
        **kwargs
    ):
        """Gets an individual page of cases.

        Args:
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status, `OPEN` or `CLOSED`. Defaults to None.
            created_at (str, optional): Filter results by case creation time range, format ISO interval.
                Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            updated_at (str, optional): Filter results by last updated time range, format ISO interval.
                Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_num (int, optional): Page number of the results. Defaults to 1.
            page_size (int, optional): Number of results to return per page. Defaults to 500.
            sort_direction (str, optional): The direction on which to sort the response,
                based on the corresponding sort key. `asc` or `desc`. Defaults to `asc`.
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number".
                Available options are name, number, createdAt, updatedAt, status, assigneeUsername, subjectUsername.

        Returns:
            :class:`py42.response.Py42Response`
        """
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

        return self._connection.get(self._uri_prefix, params=params)

    def get_all(
        self,
        name=None,
        status=None,
        created_at=None,
        updated_at=None,
        subject=None,
        assignee=None,
        page_number=1,
        page_size=items_per_page,
        sort_direction=u"asc",
        sort_key=u"number",
        **kwargs
    ):
        """Gets all cases.

        Args:
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status, `OPEN` or `CLOSED`. Defaults to None.
            created_at (str, optional): Filter results by case creation time range, format ISO interval.
                Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            updated_at (str, optional): Filter results by last updated time range, format ISO interval.
                Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_number (int, optional): Page number of the results. Defaults to 1.
            page_size (int, optional): Number of results to return per page. Defaults to 500.
            sort_direction (str, optional): The direction on which to sort the response,
                based on the corresponding sort key. `asc` or `desc`. Defaults to `asc`.
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number".
                Available options are name, number, createdAt, updatedAt, status, assigneeUsername, subjectUsername.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of cases.
        """
        return get_all_pages(
            self.get_page,
            u"cases",
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            assignee=assignee,
            subject=subject,
            page_number=page_number,
            page_size=page_size,
            sort_direction=sort_direction,
            sort_key=sort_key,
            **kwargs
        )

    def get_case(self, case_number):
        """Retrieve case details by case number.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._connection.get("{}/{}".format(self._uri_prefix, case_number))

    def export_summary(self, case_number):
        """Download case summary in a PDF file.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
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
    ):
        """Update case details for the given case number.

        Args:
            case_number (int): Case number of the case.
            name (str, optional): Name of the case. Defaults to empty string.
            subject (str, optional): A subject of the case. Defaults to empty string.
            assignee (str, optional): User UID of the assignee. Defaults to empty string.
            description (str, optional): Description of the case. Defaults to empty string.
            findings (str, optional): Notes on the case. Defaults to empty string.

        Returns:
            :class:`py42.response.Py42Response`
        """

        data = {
            u"assignee": assignee,
            u"description": description,
            u"findings": findings,
            u"name": name,
            u"subject": subject,
        }
        return self._connection.put(
            u"{}/{}".format(self._uri_prefix, case_number), data
        )
