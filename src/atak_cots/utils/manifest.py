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
