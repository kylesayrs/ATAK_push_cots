from atak_cots import CotServer


if __name__ == '__main__':
    with CotServer("localhost", 8000, directory="/tmp", wait_req_before_close=True) as server:
        server.push_cot(cot_config, "192.168.99.169", 8001)
        server.push_cot(cot_config, "192.168.99.169", 8001)
        server.push_cot(cot_config, "192.168.99.169", 8001)

        #cot_server.serve_forever()
