from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseAlreadyHasEventError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services import BaseService


class CasesFileEventsService(BaseService):

    _uri_prefix = "/api/v1/case/{0}/fileevent"

    def __init__(self, connection):
        super().__init__(connection)

    def add(self, case_number, event_id):
        """Adds an event to the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to add to the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        try:
            return self._connection.post(
                f"{self._uri_prefix.format(case_number)}/{event_id}"
            )
        except Py42BadRequestError as err:
            if "CASE_IS_CLOSED" in err.response.text:
                raise Py42UpdateClosedCaseError(err)
            elif "CASE_ALREADY_HAS_EVENT" in err.response.text:
                raise Py42CaseAlreadyHasEventError(err)
            else:
                raise

    def get(self, case_number, event_id):
        """Gets information of a specified event from the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to fetch from the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._connection.get(
            f"{self._uri_prefix.format(case_number)}/{event_id}"
        )

    def get_all(self, case_number):
        """Gets all events associated with the given case.

        Args:
            case_number (int): Case number of the case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._connection.get(self._uri_prefix.format(case_number))

    def delete(self, case_number, event_id):
        """Deletes an event from the case.

        Args:
            case_number (int): Case number of the case.
            event_id (str): Event id to remove from case.

        Returns:
            :class:`py42.response.Py42Response`
        """
        try:
            return self._connection.delete(
                f"{self._uri_prefix.format(case_number)}/{event_id}"
            )
        except Py42BadRequestError as err:
            if "CASE_IS_CLOSED" in err.response.text:
                raise Py42UpdateClosedCaseError(err)
            raise
