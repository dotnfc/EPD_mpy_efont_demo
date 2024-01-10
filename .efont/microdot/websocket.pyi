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
    """A WebSocket connection object.

    An instance of this class is sent to handler functions to manage the
    WebSocket connection.
    """
    CONT = 0
    TEXT = 1
    BINARY = 2
    CLOSE = 8
    PING = 9
    PONG = 10
    
    def __init__(self, request):
        ...
        
    async def receive(self):
        """Receive a message from the client."""
        ...
        
    async def close(self):
        """Close the websocket connection."""
        if not self.closed:  # pragma: no cover
            self.closed = True
            await self.send(b'', self.CLOSE)
        ...
        
    async def send(self, data, opcode=None):
        """Send a message to the client.

        :param data: the data to send, given as a string or bytes.
        :param opcode: a custom frame opcode to use. If not given, the opcode
                       is ``TEXT`` or ``BINARY`` depending on the type of the
                       data.
        """
        ...
        
    async def handshake(self):
        ...


