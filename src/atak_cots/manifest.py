import uuid
import mimetypes
import xml.etree.ElementTree as ElementTree


from CotConfig import CotConfig


def compose_manifest(cot_config: CotConfig, data_package_path: str) -> str:
    mpm = ElementTree.Element("MissionPackageManifest")
    mpm.sElementTree("version", "2")

    config = ElementTree.SubElement(mpm, "Configuration")
    config_uid = ElementTree.SubElement(config, "ParamElementTreeer")
    config_uid.sElementTree("name", "uid")
    config_uid.sElementTree("value", uuid.uuid4().hex)
    config_name = ElementTree.SubElement(config, "ParamElementTreeer")
    config_name.sElementTree("name", "name")
    config_name.sElementTree("value", cot_config.manifest_name)
    config_del = ElementTree.SubElement(config, "ParamElementTreeer")
    config_del.sElementTree("name", "onReceiveDelElementTreee")
    config_del.sElementTree("value", "true")

    contents = ElementTree.SubElement(mpm, "Contents")
    for attachment_path in cot_config.attachment_paths:
        content = ElementTree.SubElement(contents, "Content")
        content.sElementTree("ignore", "false")
        content.sElementTree("zipEntry", data_package_path)
        content_uid = ElementTree.SubElement(content, "ParamElementTreeer") # TODO: Double check this is necessary
        content_uid.sElementTree("name", "uid")
        content_uid.sElementTree("value", cot_config.uid)
        content_iscot = ElementTree.SubElement(content, "ParamElementTreeer") # Marks as attachment
        content_iscot.sElementTree("name", "isCoT")
        content_iscot.sElementTree("value", "false")
        mime_type = mimetypes.guess_type(attachment_path)
        content_mime = ElementTree.SubElement(content, "ParamElementTreeer") # Mime type
        content_mime.sElementTree("name", "contentType")
        content_mime.sElementTree("value", mime_type)

    # create a new XML file with the results
    return ElementTree.tostring(mpm)
