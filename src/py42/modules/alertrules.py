class AlertRulesModule(object):
    def __init__(self, microservice_client_factory):
        self.microservice_client_factory = microservice_client_factory
        self._alert_rules_manager_client = None
        self._alert_rules_client = None

    def add_user(self, rule_id, user_id, user_aliases):
        """Update alert rule criteria to apply the rule for specific user(s) for the given rule id.

        Args:
            rule_id (str): Id of a rule to be updated.
            user_id (str): A custom identifier to uniquely identify the specified user aliases
            user_aliases (str): List of Email ids/Aliases those need to be added to criteria.

        Returns
            :class:`py42.response.Py42Response`
        """
        self._alert_rules_client = self.microservice_client_factory.get_alert_rules_client()
        return self._alert_rules_client.add_user(rule_id, user_id, user_aliases)

    def remove_users(self, rule_id, user_ids):
        """Update alert rule criteria to remove users from the rule's user criteria.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.
            user_ids (list): List of custom identifiers used while adding user.
             It will remove all the aliases specified against these identifiers.

        Returns
            :class:`py42.response.Py42Response`
        """
        self._alert_rules_client = self.microservice_client_factory.get_alert_rules_client()
        return self._alert_rules_client.remove_users(rule_id, user_ids)

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the rule's user criteria.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        self._alert_rules_client = self.microservice_client_factory.get_alert_rules_client()
        return self._alert_rules_client.remove_all_users(rule_id)

    def get(self, rule_type, rule_id):
        """Fetch alert rules by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.
            rule_type (str): Either of 'exfiltration', 'cloudshare', 'typemismatch' where
              'exfiltration' implies rules related to movement of files,
              'cloudshare' implies rules related to sharing/providing public access to files
              'typemismatch' implies rules related to content and file extension mismatch.

        Returns
            :class:`py42.response.Py42Response`
        """
        self._alert_rules_client = self.microservice_client_factory.get_alert_rules_client()
        return self._alert_rules_client.get(rule_type, rule_id)

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field, default 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``, default "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
        """
        self._alert_rules_manager_client = (
            self.microservice_client_factory.get_alert_rules_manager_client()
        )
        return self._alert_rules_manager_client.get_all()

    def get_by_name(self, rule_name):
        """Fetch a rule by its name.

            Raises :class:`py42.exceptions.Py42NotFoundError` when no match is found.
        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns
            :dict: Dictionary containing rule-details.
        """
        self._alert_rules_manager_client = (
            self.microservice_client_factory.get_alert_rules_manager_client()
        )
        return self._alert_rules_manager_client.get_by_name(rule_name)
