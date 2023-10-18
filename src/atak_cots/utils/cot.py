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
