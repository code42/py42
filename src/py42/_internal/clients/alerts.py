from py42._internal.base_classes import BaseClient


class AlertClient(BaseClient):
    def __init__(self, session):
        super(AlertClient, self).__init__(session)

    def get_alert(self):
        pass

    def resolve_alert(self):
        pass

    def get_file_event_query_from_alert(self):
        uri = u"svc/api/v1/rules/query-rule-metadata"

