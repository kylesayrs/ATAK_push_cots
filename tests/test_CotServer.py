from typing import Optional, Union

import os
import time
import requests
import xml.etree.ElementTree as ElementTree

from atakcots import CotConfig, CotServer
from tests.mock import MockClient


# use global variables rather than fixtures for cleaner helper functions
_TEST_HOSTNAME = "localhost"
_TEST_SERVER_PORT = 8000
_TEST_CLIENT_PORT = 8001
_TEST_DATA_PACKAGE_DIR = "/tmp/cot_server_test"
_TEST_CLIENT_TIMEOUT = 0.1


def http_get_assert(
    location: str,
    expected_code: Union[int, None],
    expected_text: Optional[str] = None
):
    request_kwargs = {
        "url": f"http://{_TEST_HOSTNAME}:{_TEST_SERVER_PORT}{location}",
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
            s.connect((_TEST_HOSTNAME, _TEST_SERVER_PORT))

            print("READY!")
            s.close()
            break

        except:
            pass

    print("READY?")


def test_file_server_start_stop():
    server = CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR)
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

    with CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        http_get_assert("/", 200)

        with open(os.path.join(_TEST_DATA_PACKAGE_DIR, "tmp.txt"), "w") as file:
            file.write("test_data")
        http_get_assert("/tmp.txt", 200, "test_data")

    http_get_assert("/", None)


def test_restart_file_server():
    server = CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR)

    server.start()
    server.stop()
    server.start()
    http_get_assert("/", 200)

    server.stop()
    http_get_assert("/", None)


def test_restart_file_server_context():
    with CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        pass

    with CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR) as _server:
        http_get_assert("/", 200)

    http_get_assert("/", None)


def test_push_cot():
    with MockClient((_TEST_HOSTNAME, _TEST_CLIENT_PORT)) as mock_client:
        cot_config = CotConfig(
            uid="test_uid",
            latitude=0.0,
            longitude=0.0
        )

        with CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR) as server:
            server.push_cot(cot_config, _TEST_HOSTNAME, _TEST_CLIENT_PORT)
            time.sleep(0.1)  # wait for cot to be transmitted

        assert len(mock_client.connections) == 1
        assert len(mock_client.request_data) == 1

        data = ElementTree.fromstring(mock_client.request_data[0])
        assert data.tag == "event"
        assert data.get("uid") == "test_uid"
        assert data.find(".//point").attrib["lat"] == "0.0"
        assert data.find(".//point").attrib["lon"] == "0.0"


def test_push_cot_attachments():
    with MockClient((_TEST_HOSTNAME, _TEST_CLIENT_PORT)) as mock_client:
        with CotServer(_TEST_HOSTNAME, _TEST_SERVER_PORT, _TEST_DATA_PACKAGE_DIR) as server:
            attachment_path = os.path.join(_TEST_DATA_PACKAGE_DIR, "tmp.txt")
            with open(attachment_path, "w") as file:
                pass

            cot_config = CotConfig(
                uid="test_uid",
                latitude=0.0,
                longitude=0.0,
                attachment_paths=attachment_path
            )
            
            server.push_cot(cot_config, _TEST_HOSTNAME, _TEST_CLIENT_PORT)
            time.sleep(0.1)  # wait for cot to be transmitted

        assert len(mock_client.connections) == 1
        assert len(mock_client.request_data) == 1

        data = ElementTree.fromstring(mock_client.request_data[0])
        assert data.tag == "event"
        assert data.get("uid") == "test_uid"
        assert data.find(".//point").attrib["lat"] == "0.0"
        assert data.find(".//point").attrib["lon"] == "0.0"

        sender_url = (
            f"http://{_TEST_HOSTNAME}:{_TEST_SERVER_PORT}/"
            f"{os.path.basename(server._cot_dp_paths[cot_config])}"
        )
        assert data.find(".//fileshare").attrib["senderUrl"] == sender_url


# TODO: multiple cot clients with different/same data packages
def test_push_cot_clients():
    pass
