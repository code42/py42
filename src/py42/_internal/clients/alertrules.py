import json
from py42.clients import BaseClient
from py42.clients.util import get_all_pages


_ALERT_RULE_ENDPOINTS = {
    u"exfiltration": u"query-endpoint-exfiltration-rule",
    u"cloudshare": u"query-cloud-share-permissions-rule",
    u"typemismatch": u"query-file-type-mismatch-rule",
}


class AlertRulesClient(BaseClient):
    """A client to manage Alert Rules."""

    _version = u"v1"
    _resource = u"Rules/"
    _api_prefix = u"/svc/api/{0}/{1}".format(_version, _resource)

    def __init__(self, session, user_context):
        super(AlertRulesClient, self).__init__(session)
        self._user_context = user_context

    def add_user(self, rule_id, user_id, user_aliases):
        """Update alert rule criteria to apply the rule for specific user(s) for the given rule id.

        Args:
            rule_id (str): Id of a rule to be updated.
            user_id (str): User id who needs to be added to the criteria.
            user_aliases (str): Email ids/Aliases who needs to be added to criteria.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {
            u"tenantId": tenant_id,
            u"ruleId": rule_id,
            u"userList": [
                {
                    # not sure what should be passed here and its significance.
                    u"userIdFromAuthority": user_id,
                    u"userAliasList": [user_aliases],
                }
            ],
        }
        uri = u"{0}{1}".format(self._api_prefix, u"add-users")
        return self._session.post(uri, data=json.dumps(data))

    def remove_users(self, rule_id, user_ids):
        """Update alert rule criteria to remove users from the rule's user criteria.

        Args:
            rule_id (str): Id of a rule to be updated.
            user_ids (str): List of comma separated user ids who needs to be added to the criteria.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id, u"userIdList": [user_ids]}
        uri = u"{0}{1}".format(self._api_prefix, u"remove-users")
        return self._session.post(uri, data=json.dumps(data))
        pass

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the rule's user criteria.

        Args:
            rule_id (str): Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id}
        uri = u"{0}{1}".format(self._api_prefix, u"remove-all-users")
        return self._session.post(uri, data=json.dumps(data))

    def get(self, rule_type, rule_id):
        """Fetch alert rules by rule id.

        Args:
            rule_id (str): Id of a rule to be updated.
            rule_type (str): Either of 'exfiltration', 'cloudshare', 'typemismatch' where
              'exfiltration' implies rules related to movement of files,
              'cloudshare' implies rules related to sharing/providing public access to files
              'typemismatch' implies rules related to content and file extension mismatch.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {"tenantId": tenant_id, "ruleIds": [rule_id]}
        uri = u"{0}{1}".format(self._api_prefix, _ALERT_RULE_ENDPOINTS[rule_type])
        return self._session.post(uri, data=json.dumps(data))


class AlertRulesManagerClient(BaseClient):
    """A client to manage Alert Rules."""

    _version = u"v1"
    _resource = u"rules/"
    _api_prefix = u"/svc/api/{0}/{1}".format(_version, _resource)

    def __init__(self, session, user_context):
        super(AlertRulesManagerClient, self).__init__(session)
        self._user_context = user_context

    def _get_alert_rules(
        self, tenant_id, sort_key=None, sort_direction=None, page_num=None, page_size=None
    ):
        data = {
            "tenantId": tenant_id,
            "groups": [],
            "groupClause": "AND",
            "pgNum": page_num,
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        uri = u"{0}{1}".format(self._api_prefix, u"query-rule-metadata")
        return self._session.post(uri, data=json.dumps(data))

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field, default 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``, default "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
        """
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_alert_rules,
            u"ruleMetadata",
            tenant_id=tenant_id,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_by_name(self, rule_name):
        """Fetch a rule by its name.

        Args:
            rule_name (str): Name to search for, case insensitive search.

        Returns
            :class:`py42.response.Py42Response`
        """
        rules = self.get_all()

        for rule in rules:
            print(rule)
            if rule_name.lower() in rule["name"].lower():
                # TODO
                break
        pass
