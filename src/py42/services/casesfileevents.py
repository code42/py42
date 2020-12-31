from py42.services import BaseService


class CasesFileEventsService(BaseService):
    """`Rest documenation https://default-cases.core-int.cloud.code42.com/swagger-ui.html#/Cases`__ ."""
    _uri_prefix = "/api/v1/case/{0}/fileevent/"

    def __init__(self, connection):
        super(CasesFileEventsService, self).__init__(connection)

    def add_event(self, case_number, event_id):
        """Adds an event to the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to add to the case.

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._connection.post("{0}{1}".format(self._uri_prefix.format(case_number), event_id))

    def get_event(self, case_number, event_id):
        """Gets information of a specified event from the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to fetch from the case.

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._connection.get("{0}{1}".format(self._uri_prefix.format(case_number), event_id))

    def get_all_events(self, case_number):
        """Gets all events associated to the case.

        Args:
            case_number (int): Case number of the case.

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._connection.get(self._uri_prefix.format(case_number))

    def delete_event(self, case_number, event_id):
        """Deletes an event from the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to remove from case.

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._connection.delete("{0}{1}".format(self._uri_prefix.format(case_number), event_id))
