import uuid
import mimetypes
import xml.etree.ElementTree as ElementTree


from .CotConfig import CotConfig


def compose_manifest(cot_config: CotConfig, data_package_path: str) -> str:
    mpm = ElementTree.Element("MissionPackageManifest")
    mpm.set("version", "2")

    config = ElementTree.SubElement(mpm, "Configuration")
    config_uid = ElementTree.SubElement(config, "ParamElementTreeer")
    config_uid.set("name", "uid")
    config_uid.set("value", uuid.uuid4().hex)
    config_name = ElementTree.SubElement(config, "ParamElementTreeer")
    config_name.set("name", "name")
    config_name.set("value", cot_config.manifest_name)
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
