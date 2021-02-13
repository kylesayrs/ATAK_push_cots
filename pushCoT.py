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
