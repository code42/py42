class AlertModule(object):
    def __init__(self, alert_dependencies):
        self._alert_query_factory = alert_dependencies.alert_query_factory
        self._alert_client = alert_dependencies.alert_client

    @property
    def query_factory(self):
        return self._alert_query_factory

    @property
    def alert_client(self):
        return self._alert_client
