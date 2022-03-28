from datetime import datetime

from py42.choices import Choices
from py42.util import parse_timestamp_to_milliseconds_precision


class CaseStatus(Choices):
    """Constants available for setting the status of a case.

    * ``OPEN``
    * ``CLOSED``
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"


class CasesClient:
    """A client to expose cases API.

    `Rest documentation <https://developer.code42.com/api/#tag/Cases>`__
    """

    def __init__(self, cases_service, cases_file_event_service):
        self._cases_service = cases_service
        self._file_events = cases_file_event_service

    @property
    def file_events(self):
        """A collection of methods for managing file events associated with a given case.

        Returns:
            :class:`py42.services.casesfileevents.CasesFileEventsService`
        """
        return self._file_events

    def create(
        self, name, subject=None, assignee=None, description=None, findings=None
    ):
        """Creates a new case.
        `Rest documentation <https://developer.code42.com/api/#operation/createCaseUsingPOST>`__

        Args:
            name (str): Name of the case.
            subject (str, optional): User UID of a subject of a case.
            assignee (str, optional): User UID of the assignee.
            description (str, optional): Description of the case
            findings (str, optional): Observations of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._cases_service.create(
            name,
            subject=subject,
            assignee=assignee,
            description=description,
            findings=findings,
        )

    def get_page(
        self,
        page_num,
        name=None,
        status=None,
        min_create_time=None,
        max_create_time=None,
        min_update_time=None,
        max_update_time=None,
        subject=None,
        assignee=None,
        page_size=100,
        sort_direction="asc",
        sort_key="number",
        **kwargs,
    ):
        """Gets individual page of cases.
        `Rest documentation <https://developer.code42.com/api/#operation/getCasesUsingGET>`__

        Args:
            page_num (int): The page number to request.
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status. ``OPEN`` or ``CLOSED``. Defaults to None. Constants available at :class:`py42.constants.CaseStatus`.
            min_create_time (str or int or float or datetime, optional): Filter results by case creation time, start time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            max_create_time (str or int or float or datetime, optional): Filter results by case creation time, end time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            min_update_time (str or int or float or datetime, optional): Filter results by last updated time, start time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            max_update_time (str or int or float or datetime, optional): Filter results by last updated time, end time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_size (int, optional): Number of results to return per page. Defaults to 100.
            sort_direction (str, optional): The direction on which to sort the response,
                based on the corresponding sort key. `asc` or `desc`. Defaults to `asc`.
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number".
                Available options are `name`, `number`, `createdAt`, `updatedAt`, `status`, `assigneeUsername`, `subjectUsername`.

        Returns:
            :class:`py42.response.Py42Response`
        """

        created_at = _make_range(min_create_time, max_create_time)
        updated_at = _make_range(min_update_time, max_update_time)

        return self._cases_service.get_page(
            page_num,
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            subject=subject,
            assignee=assignee,
            page_size=page_size,
            sort_direction=sort_direction,
            sort_key=sort_key,
            **kwargs,
        )

    def get_all(
        self,
        name=None,
        status=None,
        min_create_time=None,
        max_create_time=None,
        min_update_time=None,
        max_update_time=None,
        subject=None,
        assignee=None,
        page_size=100,
        sort_direction="asc",
        sort_key="number",
        **kwargs,
    ):
        """Gets all cases.
        `Rest documentation <https://developer.code42.com/api/#operation/getCasesUsingGET>`__

        Args:
            name (str, optional): Filter results by case name, matches partial names. Defaults to None.
            status (str, optional): Filter results by case status. ``OPEN`` or ``CLOSED``. Defaults to None. Constants available at :class:`py42.constants.CaseStatus`.
            min_create_time (str or int or float or datetime, optional): Filter results by case creation time, start time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            max_create_time (str or int or float or datetime, optional): Filter results by case creation time, end time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            min_update_time (str or int or float or datetime, optional): Filter results by last updated time, start time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            max_update_time (str or int or float or datetime, optional): Filter results by last updated time, end time.
                 str format %Y-%m-%d %H:%M:%S. Defaults to None.
            subject (str, optional): Filter results based on User UID of a subject of a case. Defaults to None.
            assignee (str, optional): Filter results based on User UID of an assignee of a case. Defaults to None.
            page_size (int, optional): Number of results to return per page. Defaults to 100.
            sort_direction (str, optional): The direction on which to sort the response,
                based on the corresponding sort key. `asc` or `desc`. Defaults to `asc`.
            sort_key (str, optional): Values on which the response will be sorted. Defaults to "number".
                Available options are `name`, `number`, `createdAt`, `updatedAt`, `status`, `assigneeUsername`, `subjectUsername`.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of cases.
        """

        created_at = _make_range(min_create_time, max_create_time)
        updated_at = _make_range(min_update_time, max_update_time)

        return self._cases_service.get_all(
            name=name,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            subject=subject,
            assignee=assignee,
            page_size=page_size,
            sort_direction=sort_direction,
            sort_key=sort_key,
            **kwargs,
        )

    def get(self, case_number):
        """Retrieve case details by case number.
        `Rest documentation <https://developer.code42.com/api/#operation/getCaseUsingGET>`__

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._cases_service.get(case_number)

    def export_summary(self, case_number):
        """Provides case summary to download as a PDF file.
        `Rest documentation <https://developer.code42.com/api/#operation/pdfExportUsingGET>`__


        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._cases_service.export_summary(case_number)

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
        """Updates case details for the given case number.
        `Rest documentation <https://developer.code42.com/api/#operation/updateCaseUsingPUT>`__


        Args:
            case_number (int): Case number of the case.
            name (str, optional): Name of the case. Defaults to None.
            subject (str, optional): A subject of the case. Defaults to None.
            assignee (str, optional): User UID of the assignee. Defaults to None.
            description (str, optional): Description of the case. Defaults to None.
            findings (str, optional): Notes on the case. Defaults to None.
            status (str, optional): Status of the case. ``OPEN`` or ``CLOSED``. Defaults to None. Constants available at :class:`py42.constants.CaseStatus`.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._cases_service.update(
            case_number,
            name=name,
            subject=subject,
            assignee=assignee,
            description=description,
            findings=findings,
            status=status,
        )


def _make_range(begin_time, end_time):
    if not begin_time and not end_time:
        return None
    if not begin_time:
        begin_time = datetime.utcfromtimestamp(0)
    if not end_time:
        end_time = datetime.utcnow()
    end = parse_timestamp_to_milliseconds_precision(end_time)
    start = parse_timestamp_to_milliseconds_precision(begin_time)
    return f"{start}/{end}"
