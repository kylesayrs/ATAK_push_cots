import os
import uuid
import zipfile
import mimetypes
import xml.etree.ElementTree as ElementTree

from .CotConfig import CotConfig


def create_data_package(cot_config: CotConfig, directory: str) -> str:
    # create zip file as data package
    data_package_path = os.path.join(directory, f"{hash(cot_config)}.zip")
    zip_file = zipfile.ZipFile(data_package_path, "w", zipfile.ZIP_DEFLATED)

    # compose manifest
    manifest_text = compose_manifest(cot_config, data_package_path)

    # write manifest and attachment files to zip file
    zip_file.writestr(os.path.join("MANIFEST", "manifest.xml"), manifest_text)
    for attachment_path in cot_config.attachment_paths:
        zip_file.write(attachment_path)

    return data_package_path


def compose_manifest(cot_config: CotConfig, data_package_path: str) -> str:
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
        content.set("zipEntry", data_package_path)

        content_uid = ElementTree.SubElement(content, "ParamElementTreeer") # TODO: Double check this is necessary
        content_uid.set("name", "uid")
        content_uid.set("value", cot_config.uid)

        content_iscot = ElementTree.SubElement(content, "ParamElementTreeer") # Marks as attachment
        content_iscot.set("name", "isCoT")
        content_iscot.set("value", "false")

        content_mime = ElementTree.SubElement(content, "ParamElementTreeer") # Mime type
        content_mime.set("name", "contentType")
        content_mime.set("value", mimetypes.guess_type(attachment_path))

    # create a new XML file with the results
    return ElementTree.tostring(mpm)
