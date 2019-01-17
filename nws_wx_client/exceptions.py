"""
WxAPI Exceptions
"""

class WxAPIException(Exception):
    """Base class for exceptions in this module"""
    def __init__(self, message):
        self.message = message

class InvalidFormat(WxAPIException):
    """The format provided is invalid"""

class FormatNotAllowed(WxAPIException):
    """The format provided is not allowed by this endpoint"""

class APIError(WxAPIException):
    """The API returned an error"""
