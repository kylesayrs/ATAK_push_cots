import time
import pytest
import xml.etree.ElementTree as ElementTree

from atakcots import CotConfig, push_cot
from tests.mock import MockClient


# use global variables rather than fixtures for cleaner helper functions
_TEST_ADDRESS = "localhost"
_TEST_CLIENT_PORT = 8001


def test_push_cot():
    with MockClient((_TEST_ADDRESS, _TEST_CLIENT_PORT)) as mock_client:
        cot_config = CotConfig(
            uid="test_uid",
            latitude=0.0,
            longitude=0.0
        )

        push_cot(cot_config, _TEST_ADDRESS, _TEST_CLIENT_PORT)
        time.sleep(0.1)  # wait for cot to be transmitted

        assert len(mock_client.connections) == 1
        assert len(mock_client.request_data) == 1

        data = ElementTree.fromstring(mock_client.request_data[0])
        assert data.tag == "event"
        assert data.get("uid") == "test_uid"
        assert data.find(".//point").attrib["lat"] == "0.0"
        assert data.find(".//point").attrib["lon"] == "0.0"


def test_push_cot_attachments():
    cot_config = CotConfig(
        uid="test_uid",
        latitude=0.0,
        longitude=0.0,
        attachment_paths="some_file.txt"
    )

    with pytest.raises(ValueError):
        push_cot(cot_config, _TEST_ADDRESS, _TEST_CLIENT_PORT)


# TODO: multiple cot clients
def test_push_cot_clients():
    pass
