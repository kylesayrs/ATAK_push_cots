import time
from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=34.850132,
        longitude=137.120065,
        attachment_paths="sandeot.png"
    )
        
    server = CotServer("localhost", 8000)
    print(server.stat())

    server.push_cot(cot_config, "192.168.99.169", 8001)
    while server.stat()[cot_config].num_requests <= 0:
        time.sleep(0.1)

    server.close()
    print(server.stat())
