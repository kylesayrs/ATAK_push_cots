from typing import Union, List

import os


class CoTServer:
    def __init__(
        self,
        host: str,
        port: int,
        file_directory: str,
        await_requests: bool = True,
        clean_after_exit: bool = True
    ) -> None:
        self.file_directory = file_directory
        
        # begin serving in thread

        # track all push_cot calls. List all calls with sender_uid and cot uid
        # if await_requests, wait for all calls to get corresponding requests
        # before exiting

        if await_requests:
            


    def push_cot(
        self,
        uid: str,
        latitude: int,
        longitude: int,
        attachment_path: Union[str, List[str]],
        **cot_kwargs
    ):
        if uid in self._get_cot_uids():
            raise ValueError("")

        # create and save data package        
        data_package_path = _create_data_package(attachment_path)
        
        # Compose message
        message = composeMessage(uid, lat, lon, data_package_path)

        # Send message
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = sock.connect((IP, PORT))
        sock.send(message)


    def serve_forever(self):
        while True:
            pass  # catch keyboard interrupt


    def exit(self):
        pass


    def __enter__(self):
        pass


    def __exit__(self):
        pass


    def _get_cot_uids(self):
        return os.listdir(self.file_directory)
    

    def _create_data_package() -> str:
        # copy attachments, if any

        # compose manifest
        manifest_text = composeManifest(uid, attachment_files)
        os.makedirs(manifest_dir)
        with open(manifest_path, 'wb') as manifest_file:
            manifest_file.write(manifest_text)

        # zip file

        return file_path


import os
import socket
import uuid
import datetime
import xml.etree.ElementTree as ET
import hashlib

# Directories/files
PACKAGE_FILE_NAME = 'package.zip'

# Connection to ATAK device
IP = '192.168.99.199'
PORT = 4242

# Connection to file server
SERVER_IP = '192.168.99.169'
SERVER_PORT = 8001

# Parameters that describe the map object
# Guide: https://www.mitre.org/sites/default/files/pdf/09_4937.pdf
ATTITUDE = 'x'
DIMENSION = 'G'
HOW = 'm-g'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
STALE_DURATION = 10
CALLSIGN = 'Survivor'
SENDER_UID = 'sender_uid'
SENDER_CALLSIGN = 'Headquarters'
FILESHARE_NAME = 'Attachment Datapack'


def calcSize(file_path):
    return os.path.getsize(file_path)

# Stolen from: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def calcHash(file_path):
    hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        data = f.read(65536)
        while data:
            hash.update(data)
            data = f.read(65536)

    return hash.hexdigest()


import os
import shutil
import xml.etree.ElementTree as ET
import uuid
import magic
import zipfile

# Directories/files
ATTACHMENTS_DIR = 'attachments'
PACKAGE_DIR = '.package'
PACKAGES_DIR = 'packages'
PACKAGE_FILE_NAME = 'package.zip'

# Arbitrary manifest parameters
MANIFEST_NAME = 'Manifest Name'
MANIFEST_UID = uuid.uuid4().hex

def zipPackage(uid):
    assert uid != 'MANIFEST'

    attachment_dir = os.path.join(ATTACHMENTS_DIR, uid)
    if os.path.isdir(attachment_dir):
        # Clean package dir
        if os.path.isdir(PACKAGE_DIR):
            shutil.rmtree(PACKAGE_DIR)
        os.makedirs(PACKAGE_DIR)

        # Copy attachments
        attachment_files = []
        os.makedirs(os.path.join(PACKAGE_DIR, uid))
        for file in os.listdir(attachment_dir):
            file_path = os.path.join(attachment_dir, file)
            if file[0] == '.': continue
            if not os.path.isfile(file_path): continue

            dst_path = os.path.join(PACKAGE_DIR, uid, file)
            shutil.copy2(file_path, dst_path, follow_symlinks=True)

            attachment_files.append(file)

        # Write manifest
        manifest_dir = os.path.join(PACKAGE_DIR, 'MANIFEST')
        manifest_path = os.path.join(manifest_dir, 'manifest.xml')
        manifest_text = composeManifest(uid, attachment_files)
        os.makedirs(manifest_dir)
        with open(manifest_path, 'wb') as manifest_file:
            manifest_file.write(manifest_text)

        # Clean destination dir
        zip_dst_dir = os.path.join(PACKAGES_DIR, uid)
        if os.path.isdir(zip_dst_dir):
            shutil.rmtree(zip_dst_dir)
        os.makedirs(zip_dst_dir)

        # Zip file
        zip_dst_path = os.path.join(zip_dst_dir, PACKAGE_FILE_NAME)
        zip_file = zipfile.ZipFile(zip_dst_path, 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(os.path.join(PACKAGE_DIR, 'MANIFEST', 'manifest.xml'), os.path.join('MANIFEST', 'manifest.xml'))
        for file in attachment_files:
            zip_file.write(os.path.join(PACKAGE_DIR, uid, file), os.path.join(uid, file))
        zip_file.close()

        return zip_dst_path

    else:
        print("WARNING: No attachments for {uid}".format(uid=uid))
