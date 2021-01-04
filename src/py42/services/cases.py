from py42.services import BaseService
from py42.services.util import get_all_pages


class CasesService(BaseService):
    """`Rest documentation https://default-cases.core-int.cloud.code42.com/swagger-ui.html#/Cases`__ ."""

    _uri_prefix = "/api/v1/case"

    def __init__(self, connection):
        super(CasesService, self).__init__(connection)

    def create(self, name, subject, assignee, description, findings):
        """Creates a new case.

        Args:
            name (str): Name of the case. 
            subject (str): A subject of the case.
            assignee (str): User UID of the assignee.
            description (str): Description of the case
            findings (str): Observations of the case.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {
            "assignee": assignee,
            "description": description,
            "findings": findings,
            "name": name,
            "subject": subject,
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
        page_number=1,
        page_size=100,
        sort_direction="asc",
        sort_key="number",
        **kwargs
    ):
        """Gets an individual page of cases.

        Args:
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status, "OPEN" or "CLOSED". Defaults to None.
            created_at (str, optional): Filter results by case creation time range, format ISO interval. Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            updated_at (str, optional): Filter results by last updated time range, format ISO interval. Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_number (int, optional): Page number of the results. Defaults to 1.
            page_size (int, optional): Number of results to return per page. Defaults to 100.
            sort_direction (str, optional): The direction on which to sort the response, based on the corresponding sort key. "asc" or "desc" Defaults to "asc".
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number". Available options are
             name, number, createdAt, updatedAt, status, assigneeUsername, subjectUsername

        Returns:
            :class:`py42.response.Py42Response`
        """
        param_dict = {
            "assignee": assignee,
            "createAt": created_at,
            "updatedAt": updated_at,
            "status": status,
            "subject": subject,
            "name": name,
            "pgNum": page_number,
            "pgSize": page_size,
            "srtDir": sort_direction,
            "srtKey": sort_key,
            **kwargs
        }
        params = "&".join(
            ["{0}={1}".format(key, value)
             for key, value in zip(param_dict.keys(), param_dict.values())
             if param_dict[key] is not None
             ]
        )
        return self._connection.get("{0}?{1}".format(self._uri_prefix, params))

    def get_all(
        self,
        name=None,
        status=None,
        created_at=None,
        updated_at=None,
        subject=None,
        assignee=None,
        page_number=1,
        page_size=100,
        sort_direction="asc",
        sort_key="number",
        **kwargs
    ):
        """Gets all cases.

        Args:
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status, "OPEN" or "CLOSED". Defaults to None.
            created_at (str, optional): Filter results by case creation time range, format ISO interval. Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            updated_at (str, optional): Filter results by last updated time range, format ISO interval. Defaults to None. e.g 2020-08-31T11:00:00Z/2020-09-01T15:30:00Z
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_number (int, optional): Page number of the results. Defaults to 1.
            page_size (int, optional): Number of results to return per page. Defaults to 100.
            sort_direction (str, optional): The direction on which to sort the response, based on the corresponding sort key. "asc" or "desc" Defaults to "asc".
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number". Available options are
             name, number, createdAt, updatedAt, status, assigneeUsername, subjectUsername

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
            subject=subject,
            page_number=page_number,
            page_size=page_size,
            sort_dir=sort_direction,
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
        return self._connection.get("{0}/{1}".format(self._uri_prefix, case_number))

    def export(self, case_number):
        """Download case summary in a PDF file.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri_prefix = "{0}/{1}/{2}".format(self._uri_prefix, case_number, "export")
        return self._connection.post(uri_prefix)

    def update(self, case_number, name, subject, assignee, description, findings):
        """Update case details for the given case number.

        Args:
            case_number (int): Case number of the case.
            name (str): Name of the case.
            subject (str): A subject of the case.
            assignee (str): User UID of the assignee.
            description (str): Description of the case
            findings (str): Observations of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """

        data = {
            "assignee": assignee,
            "description": description,
            "findings": findings,
            "name": name,
            "subject": subject,
        }
        return self._connection.put("{0}/{1}".format(self._uri_prefix, case_number), data)
