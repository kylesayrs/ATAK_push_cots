from typing import Optional

import os
import uuid
import hashlib
import datetime
import xml.etree.ElementTree as ElementTree

from .CotConfig import CotConfig


_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def compose_message(
    hostname: str,
    port: int,
    cot_config: CotConfig,
    data_package_path: Optional[str] = None
) -> str:
    # Initialize CoT parameters
    now = datetime.datetime.utcnow()
    now_string = datetime.datetime.utcnow().strftime(_DATETIME_FORMAT)
    stale = (now + datetime.timedelta(seconds=cot_config.stale_duration)).strftime(_DATETIME_FORMAT)

    # Build XML
    event = ElementTree.Element("event")

    event.set("version", "2.0")
    event.set("uid", cot_config.uid)
    event.set("type", f"a-{cot_config.attitude}-{cot_config.dimension}")
              
    event.set("how", cot_config.how)
    event.set("start", now_string)
    event.set("time", now_string)
    event.set("stale", stale)

    detail = ElementTree.SubElement(event, "detail")
    contact = ElementTree.SubElement(detail, "contact")
    contact.set("callsign", cot_config.callsign)
    _remarks = ElementTree.SubElement(detail, "remarks")  # TODO: add remarks

    if data_package_path is not None:
        fileshare = ElementTree.SubElement(detail, "fileshare")

        fileshare.set("name", os.path.basename(data_package_path))
        fileshare.set("filename", os.path.basename(data_package_path))
        fileshare.set("senderUrl", f"http://{hostname}:{port}/getfile?file={hash(cot_config)}")

        fileshare.set("sizeInBytes", str(os.path.getsize(data_package_path)))
        fileshare.set("sha256", get_file_hash(data_package_path))

        fileshare.set("senderUid", cot_config.sender_uid)
        fileshare.set("senderCallsign", cot_config.sender_callsign)

        ackreq = ElementTree.SubElement(detail, "ackrequest")
        ackreq.set("uid", uuid.uuid4().hex)
        ackreq.set("ackrequested", "true")
        ackreq.set("tag", os.path.basename(data_package_path))

    point = ElementTree.SubElement(event, "point")
    point.set("le", "0.0")
    point.set("ce", "1.0")
    point.set("hae", "10.0")
    point.set("lat", str(cot_config.latitude))
    point.set("lon", str(cot_config.longitude))

    return ElementTree.tostring(event)


# Stolen from: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def get_file_hash(file_path: str) -> str:
    hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        data = f.read(65536)
        while data:
            hash.update(data)
            data = f.read(65536)

    return hash.hexdigest()
