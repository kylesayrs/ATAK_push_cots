import http.server
from functools import partial
from threading import Thread


if __name__ == "__main__":
    hostname = "localhost"
    port = 8000
    directory = "/tmp/asdf"

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    httpd = http.server.HTTPServer((hostname, port), handler)

    thread = Thread(target=httpd.serve_forever)
    thread.start()
    print("started")

    print("closing?")
    httpd.shutdown()
    print("closed?")
    thread.join()
