from py42.util import get_obj_from_response


class Customer(object):
    def __init__(self, administration_client):
        self._administration_client = administration_client

    def get_current_tenant_id(self):
        try:
            response = self._administration_client.get_current_tenant()
            tenant = get_obj_from_response(response, u"data")
            return tenant.get(u"tenantUid")
        except Exception as ex:
            message = (
                u"An error occurred while trying to retrieve the current tenant ID, caused by: {0}"
            )
            message = message.format(str(ex))
            raise Exception(message)
