from py42.services import BaseService
from py42.util import get_all_pages


class CasesService(BaseService):

    _uri_prefix = "/api/v1/case"

    def __init__(connection):
        super(CasesService, self).__init__(connection)

    def create(self):
        data = ""
        self._connection.post(self._uri_prefix, data)


    def _get_page(self):
        pass


    def get_all(self, name=None, status=None, ):

        self._connection.get(self._uri_prefix, ) 


    def _get(self, case_number, **kwargs):
        data = ""
        self._connection.post(self._uri_prefix, data)


    def get_case(self, case_number):
        self._connection.get("{0}/{1}".format(self._uri_prefix, case_number) )

    
    def get_case_by_name(self, name):
        self._get_all(name=name)


    def export(self, case_number):
        uri_prefix = "{0}/{1}/{2}".format(self._uri_prefix, case_number, "export")
        data = ""
        self._connection.post(uri_prefix, data)


    def update(self, case_number):
        data = ""
        self._connection.put(self._uri_prefix, data)        

