class InvestigateModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory

    @property
    def saved_search(self):
        return self._microservice_client_factory.get_saved_search_client()
