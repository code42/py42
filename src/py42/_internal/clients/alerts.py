from py42._internal.base_classes import BaseClient


class AlertClient(BaseClient):
    _base_uri = u"/svc/api/v1/"

    def search_alerts(self, query):
        query = str(query)
        uri = self._get_uri(u"query-alerts")
        return self._default_session.post(uri, data=query)

    def _get_uri(self, resource_name):
        return u"{0}{1}".format(self._base_uri, resource_name)

    @staticmethod
    def _get_default_query():
        _filter = {u"term": u"State", u"operator": u"IS", u"value": u"OPEN"}
        return [{u"filters": [_filter], u"filterClause": u"AND"}]
