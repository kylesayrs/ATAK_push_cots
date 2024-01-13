import time
from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=34.850132,
        longitude=137.120065
    )
        
    server = CotServer("localhost", 8000)
    print(server.stat())

    server.push_cot(cot_config, "localhost", 8002)
    print(server.stat())

    while server.stat()[cot_config].num_requests <= 0:
        time.sleep(0.1)

    server.close()
    print(server.stat())
