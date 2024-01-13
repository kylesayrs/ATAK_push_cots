from types import TracebackType
from typing import Optional

import socket


class SocketConnection:
    """
    Wraps tcp socket with context

    :param hostname: hostname for socket connection
    :param port: port for socket connection
    :param timeout: tcp socket connection timeout
    """
    def __init__(self, hostname: str, port: int, timeout: Optional[float] = None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._socket.connect((hostname, port))


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


if __name__ == "__main__":
    with SocketConnection("localhost", 8001) as socket_connection:
        socket_connection.send("asdf")
