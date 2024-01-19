import os
import uuid
import zipfile
import mimetypes
import xml.etree.ElementTree as ElementTree

from .CotConfig import CotConfig


def create_data_package(cot_config: CotConfig, directory: str) -> str:
    """
    Creates a zip file which serves as a data package. The zip file contains
    a manifest file which describes how to handle the data in the package as
    well as all the attachments which are served as a part of the cot message.

    :param cot_config: cursor on target message information
    :param directory: directory in which data package file should be stored 
    :return: path to data package file in directory
    """
    # create zip file as data package
    data_package_path = os.path.join(directory, f"{hash(cot_config):x}.zip")
    # TODO: check if necessary
    if os.path.exists(data_package_path):
        os.remove(data_package_path)
    zip_file = zipfile.ZipFile(data_package_path, "w", zipfile.ZIP_DEFLATED)

    # compose manifest
    manifest_text = compose_manifest(cot_config)

    # write manifest and attachment files to zip file
    zip_file.writestr(os.path.join("MANIFEST", "manifest.xml"), manifest_text)
    for attachment_path in cot_config.attachment_paths:
        # arcname should match the zipEntry value in the manifest
        zip_file.write(attachment_path, get_attachment_arcname(cot_config, attachment_path))

    return data_package_path


def compose_manifest(cot_config: CotConfig) -> str:
    """
    Compose a manifest file which describes to the atak client what attachments
    are available and how to handle them

    :param cot_config: cursor on target message information
    :param data_package_path: path to data package file
    :return: string representing manifest xml data
    """
    mpm = ElementTree.Element("MissionPackageManifest")
    mpm.set("version", "2")

    config = ElementTree.SubElement(mpm, "Configuration")
    config_uid = ElementTree.SubElement(config, "Parameter")
    config_uid.set("name", "uid")
    config_uid.set("value", uuid.uuid4().hex)
    config_name = ElementTree.SubElement(config, "Parameter")
    config_name.set("name", "name")
    config_name.set("value", cot_config.package_name)
    config_del = ElementTree.SubElement(config, "Parameter")
    config_del.set("name", "onReceiveDelElementTreee")
    config_del.set("value", "true")

    contents = ElementTree.SubElement(mpm, "Contents")
    for attachment_path in cot_config.attachment_paths:
        content = ElementTree.SubElement(contents, "Content")
        content.set("ignore", "false")
        content.set("zipEntry", get_attachment_arcname(cot_config, attachment_path))

        content_uid = ElementTree.SubElement(content, "Parameter") # TODO: Double check this is necessary
        content_uid.set("name", "uid")
        content_uid.set("value", cot_config.uid)

        content_iscot = ElementTree.SubElement(content, "Parameter") # Marks as attachment
        content_iscot.set("name", "isCoT")
        content_iscot.set("value", "false")

        content_mime = ElementTree.SubElement(content, "Parameter") # Mime type
        content_mime.set("name", "contentType")
        content_mime.set("value", mimetypes.guess_type(attachment_path)[0])

    return ElementTree.tostring(mpm)


def get_attachment_arcname(cot_config: CotConfig, attachment_path: str) -> str:
    """
    CoT attachments must be placed in a folder with the CoT uid
    """
    path_hash = hash(attachment_path)
    extension = os.path.splitext(attachment_path)[1]

    return os.path.join(cot_config.uid, f"{path_hash}{extension}")
