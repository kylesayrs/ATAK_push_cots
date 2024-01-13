
import socket


class SocketConnection:
    def __init__(self, hostname: str, port: int) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection = self._socket.connect((hostname, port))


    def send(self, message: str):
        self._connection.send(message)


    def __enter__(self) -> "SocketConnection":
        return self
    

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        print(type(_exc_type))
        print(type(_exc_val))
        print(type(_exc_tb))
        raise NotImplementedError()


if __name__ == "__main__":
    with SocketConnection("localhost", 8001) as socket_connection:
        socket_connection.send("asdf")
