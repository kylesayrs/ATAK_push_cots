import os
from http.server import BaseHTTPRequestHandler
import socketserver
from urllib.parse import urlparse

PACKAGES_DIR = 'packages'
PACKAGE_FILE_NAME = 'package.zip'

class Handler(BaseHTTPRequestHandler):

    # Runs when a get request is received
    def do_GET(self):
        try:
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))

            if 'file' in query_components:
                file_path = os.path.join(PACKAGES_DIR, query_components['file'], PACKAGE_FILE_NAME)

                if os.path.isfile(file_path):
                    # Sends a 200 response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/zip')
                    self.end_headers()

                    f = open(file_path,'rb')
                    data = f.read()
                    self.wfile.write(data)
                else:
                    # Sends a 404 response
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write('package not found')
            else:
                # Sends a 400 response
                self.send_response(400)
                self.end_headers()
                self.wfile.write('must include query')

        except:
            self.send_response(500)
            self.end_headers()

server = socketserver.TCPServer(('0.0.0.0', 8001), Handler)
server.serve_forever()
