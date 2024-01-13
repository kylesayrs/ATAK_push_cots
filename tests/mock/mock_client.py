from typing import Tuple

import socketserver


class RecordingTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Record connection details
        self.server.connections.append(self.client_address)

        # Parse data
        data = self.request.recv(1024).strip()
        received_message = data.decode("utf-8")
        print(received_message)

        # Record requestt data
        self.server.request_data.append(received_message)


class MockClient(socketserver.TCPServer):
    def __init__(self, server_address: Tuple[str, int]):
        super().__init__(server_address, RecordingTCPHandler)
        self.connections = []
        self.request_data = []


if __name__ == "__main__":
    mock_server = MockClient(("localhost", 8001))

    try:
        # Serve forever
        mock_server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        mock_server.server_close()
