class CoTServer:
    def __init__(self, host: str, port: int, file_directory: str) -> None:
        pass


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

def pushCoT(uid, lat, lon, file_path=None):
    # Compose message
    message = composeMessage(uid, lat, lon, file_path=file_path)
    print(message.decode("utf-8"))

    # Send message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = sock.connect((IP, PORT))
    sock.send(message)

def composeMessage(uid, lat, lon, file_path=None):
    # Initialize CoT parameters
    now = datetime.datetime.utcnow()
    start = now.strftime(DATETIME_FORMAT)
    time = now.strftime(DATETIME_FORMAT)
    stale = (now + datetime.timedelta(minutes=STALE_DURATION)).strftime(DATETIME_FORMAT)
    if file_path:
        size = str(calcSize(file_path))
        hash = str(calcHash(file_path))

    # Build XML
    event = ET.Element('event')
    event.set('version', '2.0')
    event.set('uid', uid)
    event.set('type', "a-{attitude}-{dimension}".format(attitude=ATTITUDE,
                                                        dimension=DIMENSION))
    event.set('how', HOW)
    event.set('start', start)
    event.set('time', time)
    event.set('stale', stale)

    detail = ET.SubElement(event, 'detail')
    contact = ET.SubElement(detail, 'contact')
    contact.set('callsign', CALLSIGN)
    remarks = ET.SubElement(detail, 'remarks')

    if file_path:
        fileshare = ET.SubElement(detail, 'fileshare')
        fileshare.set('filename', PACKAGE_FILE_NAME)
        url = 'http://{ip}:{port}/getfile?file={uid}&sender={sender}'\
              .format(ip=SERVER_IP, port=SERVER_PORT, uid=uid, sender=SENDER_CALLSIGN)
        fileshare.set('senderUrl', url)
        fileshare.set('sizeInBytes', size)
        fileshare.set('sha256', hash)
        fileshare.set('senderUid', SENDER_UID)
        fileshare.set('senderCallsign', SENDER_CALLSIGN)
        fileshare.set('name', FILESHARE_NAME)

        ackreq = ET.SubElement(detail, 'ackrequest')
        ackreq.set('uid', uuid.uuid4().hex)
        ackreq.set('ackrequested', 'true')
        ackreq.set('tag', PACKAGE_FILE_NAME)

    point = ET.SubElement(event, 'point')
    point.set('le', '0.0')
    point.set('ce', '1.0')
    point.set('hae', '10.0')
    point.set('lat', str(lat))
    point.set('lon', str(lon))

    return ET.tostring(event)

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

def composeManifest(uid, attachment_files):
    mpm = ET.Element('MissionPackageManifest')
    mpm.set('version', '2')

    config = ET.SubElement(mpm, 'Configuration')
    config_uid = ET.SubElement(config, 'Parameter')
    config_uid.set('name', 'uid')
    config_uid.set('value', MANIFEST_UID)
    config_name = ET.SubElement(config, 'Parameter')
    config_name.set('name', 'name')
    config_name.set('value', MANIFEST_NAME)
    config_del = ET.SubElement(config, 'Parameter')
    config_del.set('name', 'onReceiveDelete')
    config_del.set('value', 'true')

    contents = ET.SubElement(mpm, 'Contents')
    for file in attachment_files:
        file_path = os.path.join(PACKAGE_DIR, uid, file)
        local_path = os.path.join(uid, file)
        content = ET.SubElement(contents, 'Content')
        content.set('ignore', 'false')
        content.set('zipEntry', local_path)
        content_uid = ET.SubElement(content, 'Parameter') # TODO: Double check this is necessary
        content_uid.set('name', 'uid')
        content_uid.set('value', uid)
        content_iscot = ET.SubElement(content, 'Parameter') # Marks as attachment
        content_iscot.set('name', 'isCoT')
        content_iscot.set('value', 'false')
        mime_type = magic.Magic(mime=True).from_file(file_path)
        content_mime = ET.SubElement(content, 'Parameter') # Mime type
        content_mime.set('name', 'contentType')
        content_mime.set('value', mime_type)

    # create a new XML file with the results
    return ET.tostring(mpm)
