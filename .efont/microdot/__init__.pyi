"""
Module: 'microdot.__init__'
"""

from typing import Any
from _typeshed import Incomplete

def abort(*args, **kwargs) -> Incomplete:
    ...

@classmethod
def send_file(cls, *args, **kwargs) -> Incomplete:
    ...

@classmethod
def redirect(cls, *args, **kwargs) -> Incomplete:
    ...


class Response():
    default_content_type = 'text/plain' # type: str
    send_file_buffer_size = 1024 # type: int
    types_map = {} # type: dict
    def delete_cookie(self, *args, **kwargs) -> Incomplete:
        ...

    def set_cookie(self, *args, **kwargs) -> Incomplete:
        ...

    def complete(self, *args, **kwargs) -> Incomplete:
        ...

    def body_iter(self, *args, **kwargs) -> Incomplete:
        ...

    write : Incomplete ## <class 'generator'> = <generator>
    default_send_file_max_age : Incomplete ## <class 'NoneType'> = None
    @classmethod
    def send_file(cls, *args, **kwargs) -> Incomplete:
        ...

    already_handled : Incomplete ## <class 'Response'> = <Response object at 3c236a60>
    @classmethod
    def redirect(cls, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class Request():
    max_body_length = 16384 # type: int
    max_content_length = 16384 # type: int
    max_readline = 2048 # type: int
    def after_request(self, *args, **kwargs) -> Incomplete:
        ...

    form : Incomplete ## <class 'property'> = <property>
    body : Incomplete ## <class 'property'> = <property>
    json : Incomplete ## <class 'property'> = <property>
    stream : Incomplete ## <class 'property'> = <property>
    create : Incomplete ## <class 'generator'> = <generator>

    class G():
        def __init__(self, *argv, **kwargs) -> None:
            ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class Microdot():
    def after_error_request(self, *args, **kwargs) -> Incomplete:
        ...

    def errorhandler(self, *args, **kwargs) -> Incomplete:
        ...

    def after_request(self, *args, **kwargs) -> Incomplete:
        ...

    def abort(self, *args, **kwargs) -> Incomplete:
        ...

    def shutdown(self, *args, **kwargs) -> Incomplete:
        ...

    def before_request(self, *args, **kwargs) -> Incomplete:
        ...

    def route(self, *args, **kwargs) -> Incomplete:
        ...

    def default_options_handler(self, *args, **kwargs) -> Incomplete:
        ...

    def delete(self, *args, **kwargs) -> Incomplete:
        ...

    def put(self, *args, **kwargs) -> Incomplete:
        ...

    def mount(self, *args, **kwargs) -> Incomplete:
        ...

    def get(self, *args, **kwargs) -> Incomplete:
        ...

    def run(self, *args, **kwargs) -> Incomplete:
        ...

    def patch(self, *args, **kwargs) -> Incomplete:
        ...

    def post(self, *args, **kwargs) -> Incomplete:
        ...

    def find_route(self, *args, **kwargs) -> Incomplete:
        ...

    handle_request : Incomplete ## <class 'generator'> = <generator>
    dispatch_request : Incomplete ## <class 'generator'> = <generator>
    start_server : Incomplete ## <class 'generator'> = <generator>
    def __init__(self, *argv, **kwargs) -> None:
        ...

