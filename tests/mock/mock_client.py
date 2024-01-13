from typing import Tuple

import socketserver


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
        super().__init__(server_address, RecordingTCPHandler)
        self.verbose = verbose
        self.connections = []
        self.request_data = []

        if verbose:
            print(f"Listening on {server_address}")


    def server_close(self):
        if self.verbose:
            print("Shutting down...")

        super().server_close()


if __name__ == "__main__":
    mock_server = MockClient(("localhost", 8001), verbose=True)

    try:
        mock_server.serve_forever()
    except KeyboardInterrupt:
        mock_server.server_close()
