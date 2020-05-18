class AlertRulesModule(object):
    def __init__(self, microservice_client_factory):
        self.microservice_client_factory = microservice_client_factory

    @property
    def exfiltration(self):
        """A collection of methods for managing exfiltration alert rules.

        Returns:
            :class:`py42.clients.alertrules.exfiltration.ExfiltrationClient`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.exfiltration

    @property
    def cloudshare(self):
        """A collection of methods for managing cloud sharing alert rules.

        Returns:
            :class:`py42.clients.alertrules.cloud_share.CloudShareClient`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.cloudshare

    @property
    def filetypemismatch(self):
        """A collection of methods for managing file type mismatch alert rules.

        Returns:
            :class:`py42.clients.alertrules.file_type_mismatch.FileTypeMismatchClient`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.filetypemismatch

    def add_user(self, rule_id, user_id):
        """Update alert rule to monitor user aliases against the Uid for the given rule id.

        Args:
            rule_id (str): Observer Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to add to the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.add_user(rule_id, user_id)

    def remove_user(self, rule_id, user_id):
        """Update alert rule criteria to remove a user and all its aliases from a rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to remove from the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.remove_user(rule_id, user_id)

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the alert rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.remove_all_users(rule_id)

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``. Defaults to  "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of rules.
        """
        alerts_client = self.microservice_client_factory.get_alerts_client()
        return alerts_client.get_all_rules(sort_key=sort_key, sort_direction=sort_direction)

    def get_all_by_name(self, rule_name):
        """Search for matching rules by name.

        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of rules with the given name.
        """
        alerts_client = self.microservice_client_factory.get_alerts_client()
        return alerts_client.get_all_rules_by_name(rule_name)

    def get_by_observer_id(self, observer_id):
        """Get the rule with the matching observer ID.

        Args:
            observer_id (str): The observer ID of the rule to return.

        Returns
            :class:`py42.response.Py42Response`
        """
        alerts_client = self.microservice_client_factory.get_alerts_client()
        return alerts_client.get_rule_by_observer_id(observer_id)
