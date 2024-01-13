from types import TracebackType
from typing import Optional, Dict

import os
import shutil
import http.server
from threading import Thread
from functools import partial

from .CotConfig import CotConfig
from .message import compose_message
from .data_package import create_data_package
from .SocketConnection import SocketConnection


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

        self._make_empty_data_package_dir(data_package_dir)

        handler = partial(http.server.SimpleHTTPRequestHandler, directory=data_package_dir)
        self._file_server = http.server.HTTPServer((hostname, port), handler)
        self._file_server_thread = Thread(target=self._file_server.serve_forever)

        self._cot_dp_paths: Dict[CotConfig, str] = {}

    
    def start(self):
        """
        Start file server thread

        """
        self._file_server_thread.start()


    def stop(self):
        """
        Stop file server thread

        """
        self._file_server.shutdown()
        self._file_server_thread.join()


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
        if cot_config not in self._cot_dp_paths:
            data_package_path = create_data_package(cot_config, self._data_package_dir)
            self._cot_dp_paths[cot_config] = data_package_path
        
        # Compose message
        data_package_path = self._cot_dp_paths[cot_config]
        message = compose_message(cot_config, self._hostname, self._port, data_package_path)

        # Send message
        with SocketConnection(client_hostname, client_port, self._timeout) as socket_connection:
            socket_connection.send(message)
    

    def _make_empty_data_package_dir(self, data_package_dir: str):
        """
        Create a new, emtpy data package directory

        :param data_package_dir: path to data package directory
        """
        if os.path.isfile(data_package_dir):
            raise ValueError(
                f"File already exists with path {data_package_dir}, cannot "
                "create data package directory"
            )
        
        if os.path.exists(data_package_dir):
            shutil.rmtree(data_package_dir)
        
        os.makedirs(data_package_dir, exist_ok=True)
    
    
    def __enter__(self) -> "CotServer":
        self.start()
        return self
    

    def __exit__(self, _exc_type: type, exc_value: Exception, _exc_tb: TracebackType):
        self.stop()
