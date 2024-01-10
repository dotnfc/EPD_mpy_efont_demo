"""
Module: 'microdot.websocket'
"""


from typing import Any
from _typeshed import Incomplete

MUTED_SOCKET_ERRORS = [] # type: list
def websocket_wrapper(*args, **kwargs) -> Incomplete:
    ...

def with_websocket(*args, **kwargs) -> Incomplete:
    ...

websocket_upgrade : Incomplete ## <class 'generator'> = <generator>

class WebSocket():
    CLOSE = 8 # type: int
    BINARY = 2 # type: int
    PONG = 10 # type: int
    CONT = 0 # type: int
    PING = 9 # type: int
    TEXT = 1 # type: int
    receive : Incomplete ## <class 'generator'> = <generator>
    close : Incomplete ## <class 'generator'> = <generator>
    send : Incomplete ## <class 'generator'> = <generator>
    handshake : Incomplete ## <class 'generator'> = <generator>
    def __init__(self, *argv, **kwargs) -> None:
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

