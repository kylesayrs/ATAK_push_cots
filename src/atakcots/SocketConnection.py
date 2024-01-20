from types import TracebackType
from typing import Optional

import socket


class SocketConnection:
    """
    Context wrapper for tcp socket

    :param address: address for socket connection
    :param port: port for socket connection
    :param timeout: tcp socket connection timeout
    """
    def __init__(self, address: str, port: int, timeout: Optional[float] = None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._socket.connect((address, port))


    def send(self, message: str):
        """
        Send message over tcp socket

        :param message: message content
        """
        self._socket.send(message)


    def __enter__(self) -> "SocketConnection":
        return self
    

    def __exit__(self, _exc_type: type, exc_value: Exception, _exc_tb: TracebackType):
        self._socket.close()
