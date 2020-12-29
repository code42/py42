
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


    def create():
        self._cases_service.create()


    def get_all():
        self._cases_service.get_all()


    def get_case_by_name():
        self._cases_service.get_case_by_name()


    def export():
        self._cases_service.export()


    def update():
        self._cases_service.update()

