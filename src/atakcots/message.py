from typing import Optional

import os
import uuid
import hashlib
import datetime
import xml.etree.ElementTree as ElementTree

from .CotConfig import CotConfig


_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def compose_message(
    cot_config: CotConfig,
    address: Optional[str] = None,
    port: Optional[int] = None,
    data_package_path: Optional[str] = None
) -> str:
    """
    Compose a cursor on target message. Specify all of address, port, and
    data_package_path to instruct the client to request attachments from
    the data package server

    :param cot_config: cursor on target message information
    :param address: data package file server address
    :param port: data package file server port
    :param data_package_path: path to data package file
    :return: string representing cursor on target xml data
    """
    dp_args_none = [address is None, port is None, data_package_path is None]
    if any(dp_args_none) and not all(dp_args_none):
        raise ValueError(
            "Must specify all data package arguments `address`, `port`, "
            "`data_package_path`, or none at all"
        )

    now = datetime.datetime.utcnow()
    now_string = datetime.datetime.utcnow().strftime(_DATETIME_FORMAT)
    stale = (now + datetime.timedelta(seconds=cot_config.stale_duration)).strftime(_DATETIME_FORMAT)

    # create event
    event = ElementTree.Element("event")
    event.set("version", "2.0")
    event.set("uid", cot_config.uid)

    # methodology data
    event.set("type", cot_config.type)
    event.set("how", cot_config.how)
    
    # time data
    event.set("start", now_string)
    event.set("time", now_string)
    event.set("stale", stale)

    # additional data
    detail = ElementTree.SubElement(event, "detail")
    contact = ElementTree.SubElement(detail, "contact")
    contact.set("callsign", cot_config.callsign)
    _remarks = ElementTree.SubElement(detail, "remarks")  # TODO: add remarks
    _track = ElementTree.SubElement(detail, "track")  # TODO: add track

    # attachments data
    if data_package_path is not None:
        fileshare = ElementTree.SubElement(detail, "fileshare")

        fileshare.set("name", os.path.basename(data_package_path))
        fileshare.set("filename", os.path.basename(data_package_path))
        fileshare.set("senderUrl", f"http://{address}:{port}/{hash(cot_config):x}.zip")

        fileshare.set("sizeInBytes", str(os.path.getsize(data_package_path)))
        fileshare.set("sha256", hash_file_sha256(data_package_path))

        fileshare.set("senderUid", cot_config.sender_uid)
        fileshare.set("senderCallsign", cot_config.sender_callsign)

        ackreq = ElementTree.SubElement(detail, "ackrequest")
        ackreq.set("uid", uuid.uuid4().hex)
        ackreq.set("ackrequested", "true")
        ackreq.set("tag", os.path.basename(data_package_path))

    # location data
    point = ElementTree.SubElement(event, "point")
    point.set("lat", str(cot_config.latitude))
    point.set("lon", str(cot_config.longitude))
    point.set("hae", str(cot_config.altitude))
    point.set("ce", "1.0")
    point.set("le", "0.0")

    return ElementTree.tostring(event)


def hash_file_sha256(file_path: str, chunk_size: int = 65536) -> str:
    """
    Hash a file using sha256 with set chunk size

    :param file_path: path to file being hashed
    :param chunk_size: hash chunk size, use 65536 for cot application
    :return: hex string representation of sha256 hash
    """
    _hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        while data := file.read(chunk_size):
            _hash.update(data)

    return _hash.hexdigest()
