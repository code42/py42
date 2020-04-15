import json

from py42._internal.compat import str
from py42.clients import BaseClient


class DetectionListUserClient(BaseClient):
    """Administrator utility to manage High Risk employees information.

    `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Detection_list_management_APIs>`__
    """

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}".format(_api_version)
    _resource = u"/user"

    def __init__(self, session, user_context):
        super(DetectionListUserClient, self).__init__(session)
        self._user_context = user_context

    def _make_uri(self, action):
        return u"{0}{1}{2}".format(self._uri_prefix, self._resource, action)

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
               e.g u"tag1" or ["tag1", "tag2"], for python version 2.X, pass u"str" instead of "str"

        Returns:
            :class:`py42.response.Py42Response`
        """

        if type(tags) is str:
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
               e.g u"tag1" or ["tag1", "tag2"], for python version 2.X, pass u"str" instead of "str"

        Returns:
            :class:`py42.response.Py42Response`
        """
        if type(tags) is str:
            tags = [tags]

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"riskFactors": tags,
        }
        uri = self._make_uri(u"/removeriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def add_cloud_aliases(self, user_id, aliases):
        """Add one or more cloud alias.

        Args:
            user_id (str or int): The user_id whose alias(es) need to be updated.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be added.
                e.g u"x" or ["email@id", "y"], for python version 2.X, pass u"str" instead of "str"

        Returns:
            :class:`py42.response.Py42Response`
        """
        if type(aliases) is str:
            aliases = [aliases]

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"cloudUsernames": aliases,
        }
        uri = self._make_uri(u"/addcloudusernames")
        return self._session.post(uri, data=json.dumps(data))

    def remove_cloud_aliases(self, user_id, aliases):
        """Remove one or more cloud alias.

        Args:
            user_id (str or int): The user_id whose alias(es) need to be removed.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be removed.
                e.g u"x" or ["email@id", "y"], for python version 2.X, pass u"str" instead of "str"

        Returns:
            :class:`py42.response.Py42Response`
        """
        if type(aliases) is str:
            aliases = [aliases]

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
            u"cloudUsernames": aliases,
        }
        uri = self._make_uri(u"/removecloudusernames")
        return self._session.post(uri, data=json.dumps(data))
