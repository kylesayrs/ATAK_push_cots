from types import TracebackType
from typing import Union, List, Optional, Dict

import os
import copy
import time
import zipfile
from dataclasses import dataclass

from .CotConfig import CotConfig
from .message import compose_message
from .manifest import compose_manifest
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
        directory: str = "/tmp/cot_server",
        wait_req_before_close: bool = False
    ):
        self.hostname = hostname
        self.port = port
        self.directory = directory
        self.wait_req_before_close = wait_req_before_close

        os.makedirs(directory, exist_ok=True)
        self.cot_entries: Dict[CotConfig, CotEntry] = {}
    
        # TODO: start file server in separate thread


    def push_cot(
        self,
        cot_config: CotConfig,
        client_hostname: str,
        client_port: int
    ):
        # create data package if new cot
        if cot_config not in self.cot_entries:
            data_package_path = self._create_data_package(cot_config)
            self.cot_entries[cot_config] = CotEntry(data_package_path)
        
        # Compose message
        data_package_path = self.cot_entries[cot_config].data_package_path
        message = compose_message(cot_config, data_package_path)

        # Send message
        with SocketConnection(client_hostname, client_port) as socket_connection:
            socket_connection.send(message)


    def stat(self) -> Dict[CotConfig, CotEntry]:
        return {
            cot_config.copy(): copy.deepcopy(cot_entry)
            for cot_config, cot_entry in self.cots.items()
        }
    

    def _create_data_package(self, cot_config: CotConfig) -> str:
        # create zip file as data package
        data_package_path = os.path.join(self.directory, f"{hash(cot_config)}.zip")
        zip_file = zipfile.ZipFile(data_package_path, "w", zipfile.ZIP_DEFLATED)

        # compose manifest
        manifest_text = compose_manifest(cot_config, data_package_path)

        # write manifest and attachment files to zip file
        zip_file.writestr(os.path.join("MANIFEST", "manifest.xml"), manifest_text)
        for attachment_path in cot_config.attachment_paths:
            zip_file.write(attachment_path)

        return data_package_path
    
    
    def __enter__(self) -> "CotServer":
        return self
    

    def __exit__(self, _exc_type: type, _exc_val: TypeError, _exc_tb: TracebackType):
        if self.wait_req_before_close:
            while True:
                cot_been_requested = [
                    cot_entry.num_requests > 0
                    for cot_entry in self.cot_entries.values()
                ]

                if all(cot_been_requested):
                    return

                time.sleep(0.1)
