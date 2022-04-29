from py42.choices import Choices


class TrustedActivityType(Choices):
    """Constants available for setting the type of a trusted activity.

    * ``DOMAIN``
    * ``SLACK``
    """

    DOMAIN = "DOMAIN"
    SLACK = "SLACK"


class TrustedActivitiesClient:
    """A client to expose the trusted activities/data preferences API

    `Rest documentation <https://developer.code42.com/api/#tag/Trusted-Activities>`__
    """

    def __init__(self, trusted_activities_service):
        self._trusted_activities_service = trusted_activities_service

    def get_all(self, type=None, page_size=None):
        """Gets all trusted activities.
        `Rest documentation <https://developer.code42.com/api>`__

        Args:
            type (str, optional): Type of the trusted activity. Defaults to None. Constants available at :class:`py42.constants.TrustedActivityType`.
            page_size (int, optional): Number of results to return per page. Defaults to 100.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of cases.
        """
        return self._trusted_activities_service.get_all(type, page_size)

    def create(self, type, value, description=None):
        """Gets all trusted activities with the given type.
        `Rest documentation <https://developer.code42.com/api>`__

        Args:
            type (str): Type of the trusted activity. Constants available at :class:`py42.constants.TrustedActivityType`.
            value (str): The URL of the domain or name of the Slack workspace.
            description (str, optional): Description of the trusted activity.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._trusted_activities_service.create(type, value, description)

    def get(self, id):
        """Retrieve trusted activity details by given resource number.
        `Rest documentation <https://developer.code42.com/api>`__

        Args:
            id (int): Resource number of the trusted activity or domain.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._trusted_activities_service.get(id)

    def update(self, id, value=None, description=None):
        """Updates trusted activity details by given resource number.
        `Rest documentation <https://developer.code42.com/api>`__

        Args:
            id (int): Resource number of the trusted activity.
            value (str, optional): The URL of the domain or name of the Slack workspace.
            description (str, optional): Description of the trusted activity.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._trusted_activities_service.update(
            id=id, value=value, description=description
        )

    def delete(self, id):
        """Deletes a trusted activity by given resource number.
        `Rest documentation <https://developer.code42.com/api>`__

        Args:
            id (int): Resource number of the trusted activity or domain.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._trusted_activities_service.delete(id)
