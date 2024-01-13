from types import TracebackType
from typing import Tuple

import socketserver
from threading import Thread


class RecordingTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Record connection details
        self.server.connections.append(self.client_address)

        # Parse data
        data = self.request.recv(1024).strip()
        received_message = data.decode("utf-8")
        if self.server.verbose:
            print(received_message)

        # Record request data
        self.server.request_data.append(received_message)


class MockClient(socketserver.TCPServer):
    def __init__(self, server_address: Tuple[str, int], verbose: bool = False):
        self.server_address = server_address
        self.verbose = verbose

        self.connections = []
        self.request_data = []

        self._thread = None

        super().__init__(server_address, RecordingTCPHandler)


    def server_close(self):
        if self.verbose:
            print("Shutting down...")

        super().server_close()


    def start(self):
        self._thread = Thread(target=self.serve_forever)
        self._thread.start()

        if self.verbose:
            print(f"Listening on {self.server_address}")


    def stop(self):
        self.shutdown()
        self.server_close()
        self._thread.join()
        self._thread = None


    def __enter__(self) -> "MockClient":
        self.start()
        return self
    

    def __exit__(self, _exc_type: type, exc_value: Exception, _exc_tb: TracebackType):
        self.stop()


if __name__ == "__main__":
    with MockClient(("localhost", 8001), verbose=True) as mock_server:
        try:
            while True: pass 
        except KeyboardInterrupt:
            pass
