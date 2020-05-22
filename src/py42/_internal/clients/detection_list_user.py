import json

from py42.clients import BaseClient
from py42.exceptions import Py42BadRequestError, Py42NotFoundError


class DetectionListUserClient(BaseClient):
    """Administrator utility to manage High Risk employees information.

    `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Detection_list_management_APIs>`__
    """

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}".format(_api_version)
    _resource = u"/user"

    def __init__(self, session, user_context, user_client):
        super(DetectionListUserClient, self).__init__(session)
        self._user_context = user_context
        self._user_client = user_client

    def _make_uri(self, action):
        return u"{0}{1}{2}".format(self._uri_prefix, self._resource, action)

    def create_if_not_exists(self, user_id):
        """Find out whether the detection list profile exists for a given uid. If not,
           if user_id is a valid uid of code42 user then it will create detection list profile
           of the user.

            Returns True when profile is created else raises error.

            Args:
                user_id (str or int): Uid of user.

            Returns:
                bool
        """
        try:
            self.get_by_id(user_id)
        except (Py42NotFoundError, Py42BadRequestError):
            user = self._user_client.get_by_uid(user_id)
            self.create(user[u"username"])
        return True

    def create(self, username):
        """Create a detection list profile for a user.

        Args:
            username (str): Username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userName": username,
            u"notes": "",
            u"riskFactors": [],
            u"cloudUsernames": [],
        }
        uri = self._make_uri(u"/create")
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, user_id):
        """Get user details by user id.

        Args:
            user_id (str or int): Id of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._user_context.get_current_tenant_id(), u"userId": user_id}
        uri = self._make_uri(u"/getbyid")
        return self._session.post(uri, data=json.dumps(data))

    def get(self, username):
        """Get user details by username.

        Args:
            username (str): Username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._user_context.get_current_tenant_id(), u"username": username}
        uri = self._make_uri(u"/getbyusername")
        return self._session.post(uri, data=json.dumps(data))

    def update_notes(self, user_id, notes):
        """Add or update notes related to the user.

        Args:
            user_id (str or int): The user_id whose notes need to be updated.
            notes (str): User profile notes.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"notes": notes,
        }
        uri = self._make_uri(u"/updatenotes")
        return self._session.post(uri, data=json.dumps(data))

    def add_risk_tags(self, user_id, tags):
        """Add one or more tags.

        Args:
            user_id (str or int): The user_id whose tag(s) needs to be updated.
            tags (str or list of str ): A single tag or multiple tags in a list to be added.
               e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.response.Py42Response`
        """

        if not isinstance(tags, (list, tuple)):
            tags = [tags]

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"riskFactors": tags,
        }
        uri = self._make_uri(u"/addriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def remove_risk_tags(self, user_id, tags):
        """Remove one or more tags.Args:

        Args:
            user_id (str or int): The user_id whose tag(s) needs to be removed.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed.
               e.g "tag1" or ["tag1", "tag2"].

        Returns:
            :class:`py42.response.Py42Response`
        """
        if not isinstance(tags, (list, tuple)):
            tags = [tags]

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"riskFactors": tags,
        }
        uri = self._make_uri(u"/removeriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def add_cloud_alias(self, user_id, alias):
        """Add a cloud alias.

        Args:
            user_id (str or int): The user_id whose alias needs to be updated.
            alias (str): An alias to be added.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"cloudUsernames": [alias],
        }
        uri = self._make_uri(u"/addcloudusernames")
        return self._session.post(uri, data=json.dumps(data))

    def remove_cloud_alias(self, user_id, alias):
        """Remove one or more cloud alias.

        Args:
            user_id (str or int): The user_id whose alias needs to be removed.
            alias (str): An alias to be removed.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"cloudUsernames": [alias],
        }
        uri = self._make_uri(u"/removecloudusernames")
        return self._session.post(uri, data=json.dumps(data))
