from typing import Optional, Union

import pytest
import os
import requests

from atakcots import CotConfig, CotServer


# use global variables rather than fixtures for cleaner helper functions
_TEST_HOSTNAME = "localhost"
_TEST_PORT = 8000
_TEST_DATA_PACKAGE_DIR = "/tmp/cot_server_test"
_TEST_CLIENT_TIMEOUT = 0.1


def http_get_assert(
    location: str,
    expected_code: Union[int, None],
    expected_text: Optional[str] = None
):
    request_kwargs = {
        "url": f"http://{_TEST_HOSTNAME}:{_TEST_PORT}{location}",
        "timeout": _TEST_CLIENT_TIMEOUT
    }

    if expected_code is None:
        try:
            response = requests.get(**request_kwargs)
            assert False, "Did not raise exception as expected"

        except Exception as exception:
            assert (
                isinstance(exception, requests.exceptions.ReadTimeout) or
                isinstance(exception, requests.exceptions.ConnectionError)
            )
    else:
        response = requests.get(**request_kwargs)
        assert response.status_code == expected_code

        if expected_text is not None:
            assert response.text == expected_text


def await_socket_available():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            s.connect((_TEST_HOSTNAME, _TEST_PORT))

            print("READY!")
            s.close()
            break

        except:
            pass

    print("READY?")


def test_file_server_start_stop():
    server = CotServer(_TEST_HOSTNAME, _TEST_PORT, _TEST_DATA_PACKAGE_DIR)
    http_get_assert("/", None)

    server.start()
    http_get_assert("/", 200)
    
    with open(os.path.join(_TEST_DATA_PACKAGE_DIR, "tmp.txt"), "w") as file:
        file.write("test_data")
    http_get_assert("/tmp.txt", 200, "test_data")

    server.stop()
    http_get_assert("/", None)


def test_file_server_context():
    http_get_assert("/", None)

    with CotServer(_TEST_HOSTNAME, _TEST_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        http_get_assert("/", 200)

        with open(os.path.join(_TEST_DATA_PACKAGE_DIR, "tmp.txt"), "w") as file:
            file.write("test_data")
        http_get_assert("/tmp.txt", 200, "test_data")

    http_get_assert("/", None)


def test_restart_file_server():
    server = CotServer(_TEST_HOSTNAME, _TEST_PORT, _TEST_DATA_PACKAGE_DIR)

    server.start()
    server.stop()
    server.start()
    http_get_assert("/", 200)

    server.stop()
    http_get_assert("/", None)


def test_restart_file_server_context():
    with CotServer(_TEST_HOSTNAME, _TEST_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        pass

    with CotServer(_TEST_HOSTNAME, _TEST_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        http_get_assert("/", 200)

    http_get_assert("/", None)
