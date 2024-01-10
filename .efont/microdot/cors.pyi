"""
Module: 'microdot.cors'
"""

from typing import Any
from _typeshed import Incomplete


class CORS():
    """Add CORS headers to HTTP responses.

    :param app: The application to add CORS headers to.
    :param allowed_origins: A list of origins that are allowed to make
                            cross-site requests. If set to '*', all origins are
                            allowed.
    :param allow_credentials: If set to True, the
                            ``Access-Control-Allow-Credentials`` header will
                            be set to ``true`` to indicate to the browser
                            that it can expose cookies and authentication
                            headers.
    :param allowed_methods: A list of methods that are allowed to be used when
                            making cross-site requests. If not set, all methods
                            are allowed.
    :param expose_headers: A list of headers that the browser is allowed to
                        exposed.
    :param allowed_headers: A list of headers that are allowed to be used when
                            making cross-site requests. If not set, all headers
                            are allowed.
    :param max_age: The maximum amount of time in seconds that the browser
                    should cache the results of a preflight request.
    :param handle_cors: If set to False, CORS headers will not be added to
                        responses. This can be useful if you want to add CORS
                        headers manually.
    """
    def __init__(self, *argv, **kwargs) -> None:
        ...
        
    def get_cors_headers(self, request):
        """Return a dictionary of CORS headers to add to a given request.

        :param request: The request to add CORS headers to.
        """
        ...

    def initialize(self, app, handle_cors=True):
        """Initialize the CORS object for the given application.

        :param app: The application to add CORS headers to.
        :param handle_cors: If set to False, CORS headers will not be added to
                            responses. This can be useful if you want to add
                            CORS headers manually.
        """
        ...
        
    def options_handler(self, request):
        ...

    def after_request(self, request, response):
        ...



