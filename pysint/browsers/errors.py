import aiohttp

class BrowserException(Exception):
    """Base exception class for Browsers module

    Ideally designed to catch and handle any exception raised from this module
    """
    pass

class HTTPException(BrowserException):
    """Exception that's raised when a HTTP request operation fails.

    """
    def __init__(self, message, resp: aiohttp.ClientResponse.status):
        self.message = message
        self.status = resp



