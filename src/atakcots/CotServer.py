from types import TracebackType
from typing import Optional, Dict, List

import os
import copy
from dataclasses import dataclass, field

from .CotConfig import CotConfig
from .message import compose_message
from .data_package import create_data_package
from .SocketConnection import SocketConnection


@dataclass
class CotEntry:
    """
    Stores information about a particular cot/data package endpoint
    
    :param data_package_path: path to associated data package
    :param client_requests: list of all clients ips which have requested the
        data package in order of request
    """
    data_package_path: Optional[str] = None
    client_requests: List[str] = field(default_factory=lambda: [])


class CotServer:
    """
    CotServer handles the creation of data packages which contain attachments,
    the sending of cursor on target messages over TCP socket, and the serving of
    said data packages.

    ```
    with CotServer("localhost", 8000) as server:
        server.push_cot(cot_config, "client_hostname", 8001)
    ```

    :param hostname: hostname where cot data packages are served from
    :param port: port where cot data packages are served from
    :param data_package_dir: path to directory where data package files are stored
    :param timeout: defines timeout for sending cot messages over tcp socket
    """
    def __init__(
        self,
        hostname: str,
        port: int,
        data_package_dir: str = "/tmp/cot_server",
        timeout: Optional[float] = None
    ):
        self._hostname = hostname
        self._port = port
        self._data_package_dir = data_package_dir
        self._timeout = timeout

        os.makedirs(data_package_dir, exist_ok=True)
        self._cot_entries: Dict[CotConfig, CotEntry] = {}

    
    def start(self):
        # TODO: make sure file server is secure
        # TODO: start file server in thread
        pass


    def stop(self):
        # TODO: stop server and thread
        pass


    def push_cot(
        self,
        cot_config: CotConfig,
        client_hostname: str,
        client_port: int
    ):
        """
        Push cursor on target message to client with associated data package

        :param cot_config: cursor on target message information
        :param client_hostname: cot destination hostname
        :param client_port: cot destination port
        """
        # create data package if new cot
        if cot_config not in self._cot_entries:
            data_package_path = create_data_package(cot_config, self._data_package_dir)
            self._cot_entries[cot_config] = CotEntry(data_package_path)
        
        # Compose message
        data_package_path = self._cot_entries[cot_config].data_package_path
        message = compose_message(cot_config, self._hostname, self._port, data_package_path)

        # Send message
        with SocketConnection(client_hostname, client_port, self._timeout) as socket_connection:
            socket_connection.send(message)


    def stat(self) -> Dict[CotConfig, CotEntry]:
        """
        Get statistics about cot endpoints

        :return: dictionary mapping cot configs to endpoint data
        """
        return {
            cot_config.model_copy(deep=True): copy.deepcopy(cot_entry)
            for cot_config, cot_entry in self._cot_entries.items()
        }
    
    
    def __enter__(self) -> "CotServer":
        self.start()
        return self
    

    def __exit__(self, _exc_type: type, exc_value: Exception, _exc_tb: TracebackType):
        self.stop()
