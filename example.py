from atak_cots import CoTServer


if __name__ == '__main__':
    cot_server = CoTServer(host, port, file_directory)
    cot_server.pushCoT(
        "CoT UID",
        34.850132,
        137.120065,
        callsign="Test CoT"
    )
    cot_server.serve_forever()
