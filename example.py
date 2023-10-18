from atak_cots import CoTServer


if __name__ == '__main__':
    with CoTServer(host, port, file_directory, await_requests=True) as cot_server:
        cot_server.push_cot(
            "CoT UID",
            34.850132,
            137.120065,
            attachment,
            callsign="Test CoT"
        )

        #cot_server.serve_forever()
