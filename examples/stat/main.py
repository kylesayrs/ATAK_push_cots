import time
from atakcots import CotConfig, CotServer

if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=34.850132,
        longitude=137.120065
    )
        
    with CotServer("localhost", 8000) as server:
        print(server.stat())
        # {}

        server.push_cot(cot_config, "192.168.99.1", 8001)
        print(server.stat())
        # {CotConfig(uid='My_Message', ...): CotEntry(... client_requests=[])}

        time.sleep(5)  # wait for client to request
        print(server.stat())
        # {CotConfig(uid='My_Message', ...): CotEntry(... client_requests=["192.168.1.1"])}
