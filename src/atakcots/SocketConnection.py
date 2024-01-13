from types import TracebackType

import socket


class SocketConnection:
    def __init__(self, hostname: str, port: int, timeout: float = None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
    
        self._connection = self._socket.connect((hostname, port))


    def send(self, message: str):
        self._connection.send(message)


    def __enter__(self) -> "SocketConnection":
        return self
    

    def __exit__(self, _exc_type: type, _exc_val: TypeError, _exc_tb: TracebackType):
        self._socket.close()


if __name__ == "__main__":
    with SocketConnection("localhost", 8001) as socket_connection:
        socket_connection.send("asdf")
