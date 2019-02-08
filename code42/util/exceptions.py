
# class SDKError(Exception):
#     def __init__(self, message, cause):
#         self.cause = cause
#         if cause:
#             message = message + ", caused by " + "\n\t" + repr(self)
#         super(SDKError, self).__init__(message)
#
#     def __repr__(self):
#         return self.cause.__class__.__name__ + ": " + self.cause.message
#
#
# class HTTPError(SDKError):
#     def __init__(self, message, cause, **kwargs):
#         super(HTTPError, self).__init__(message, cause)
#         response = kwargs.pop('response', None)
#         if response:
#             self.response = response
#             self.request = self.response.request

