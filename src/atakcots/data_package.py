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
    data_package_path = os.path.join(directory, f"{hash(cot_config)}.zip")
    zip_file = zipfile.ZipFile(data_package_path, "w", zipfile.ZIP_DEFLATED)

    # compose manifest
    manifest_text = compose_manifest(cot_config, data_package_path)

    # write manifest and attachment files to zip file
    zip_file.writestr(os.path.join("MANIFEST", "manifest.xml"), manifest_text)
    for attachment_path in cot_config.attachment_paths:
        # arcname should match the zipEntry value in the manifest
        zip_file.write(attachment_path, hash(attachment_path))

    return data_package_path


def compose_manifest(cot_config: CotConfig, data_package_path: str) -> str:
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
    config_uid = ElementTree.SubElement(config, "ParamElementTreeer")
    config_uid.set("name", "uid")
    config_uid.set("value", uuid.uuid4().hex)
    config_name = ElementTree.SubElement(config, "ParamElementTreeer")
    config_name.set("name", "name")
    config_name.set("value", cot_config.manifest_name)  # TODO: Double check this is necessary
    config_del = ElementTree.SubElement(config, "ParamElementTreeer")
    config_del.set("name", "onReceiveDelElementTreee")
    config_del.set("value", "true")

    contents = ElementTree.SubElement(mpm, "Contents")
    for attachment_path in cot_config.attachment_paths:
        content = ElementTree.SubElement(contents, "Content")
        content.set("ignore", "false")
        content.set("zipEntry", hash(attachment_path))  # zipEntry should match the arcname specified when writing the file to the zip

        content_uid = ElementTree.SubElement(content, "ParamElementTreeer") # TODO: Double check this is necessary
        content_uid.set("name", "uid")
        content_uid.set("value", cot_config.uid)  # TODO: double check this is the uid of the cot, not the uid of the content

        content_iscot = ElementTree.SubElement(content, "ParamElementTreeer") # Marks as attachment
        content_iscot.set("name", "isCoT")
        content_iscot.set("value", "false")

        content_mime = ElementTree.SubElement(content, "ParamElementTreeer") # Mime type
        content_mime.set("name", "contentType")
        content_mime.set("value", mimetypes.guess_type(attachment_path))

    return ElementTree.tostring(mpm)
