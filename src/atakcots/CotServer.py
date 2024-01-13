from types import TracebackType
from typing import Optional, Dict

import os
import copy
import time
from dataclasses import dataclass

from .CotConfig import CotConfig
from .message import compose_message
from .data_package import create_data_package
from .SocketConnection import SocketConnection


@dataclass
class CotEntry:
    data_package_path: Optional[str] = None
    num_requests: int = 0


class CotServer:
    def __init__(
        self,
        hostname: str,
        port: int,
        data_package_dir: str = "/tmp/cot_server",
        wait_req_before_close: bool = False
    ):
        self._hostname = hostname
        self._port = port
        self._data_package_dir = data_package_dir
        self._wait_req_before_close = wait_req_before_close

        os.makedirs(data_package_dir, exist_ok=True)
        self._cot_entries: Dict[CotConfig, CotEntry] = {}

    
    def start(self, ):
        # TODO: start file server in thread
        pass


    def stop(self):
        if self._wait_req_before_close:
            while True:
                cot_been_requested = [
                    cot_entry.num_requests > 0
                    for cot_entry in self._cot_entries.values()
                ]

                if all(cot_been_requested):
                    return

                time.sleep(0.1)

        # TODO: stop server and thread


    def push_cot(
        self,
        cot_config: CotConfig,
        client_hostname: str,
        client_port: int
    ):
        # create data package if new cot
        if cot_config not in self._cot_entries:
            data_package_path = create_data_package(cot_config, self._data_package_dir)
            self._cot_entries[cot_config] = CotEntry(data_package_path)
        
        # Compose message
        data_package_path = self._cot_entries[cot_config].data_package_path
        message = compose_message(self._hostname, self._port, cot_config, data_package_path)

        # Send message
        with SocketConnection(client_hostname, client_port) as socket_connection:
            socket_connection.send(message)


    def stat(self) -> Dict[CotConfig, CotEntry]:
        return {
            cot_config.model_dump(mode="python"): copy.deepcopy(cot_entry)
            for cot_config, cot_entry in self._cot_entries.items()
        }
    
    
    def __enter__(self) -> "CotServer":
        self.start()
        return self
    

    def __exit__(self, _exc_type: type, exc_value: Exception, _exc_tb: TracebackType):
        if exc_value is not None:
            raise exc_value

        self.stop()
