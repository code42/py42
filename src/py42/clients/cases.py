
class CasesClient(object):

    def __init__(self, cases_service, cases_file_event_client):
        self._cases_service = cases_service
        self._file_events = cases_file_event_client

    @property
    def file_events(self):
        """A collection of method for managing cases file events.

        Returns :
            :class:`py42.services.casesfileevents.FileEventsService`
        """
        self.file_events = self._file_events

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

        self._cases_service.create(name, subject, assignee, description, findings)

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
        self._cases_service.get_all()

    def get_case_by_case_number(self, case_number):
        """Retrieve case details by case number.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._cases_service.get_case(case_number)

    def export(self, case_number):
        """Provides case summary to download as a PDF file.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._cases_service.export(case_number)

    def update(self, case_number, name, subject, assignee, description, findings):
        """Updates case details for the given case number.

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
        self._cases_service.update(case_number, name, subject, assignee, description, findings)
