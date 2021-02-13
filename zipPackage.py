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
