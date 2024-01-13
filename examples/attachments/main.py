from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=34.850132,
        longitude=137.120065,
        attachment_paths="sandeot.png"
    )
        
    with CotServer("localhost", 8000) as server:
        server.push_cot(cot_config, "localhost", 8001)
        server.push_cot(cot_config, "localhost", 8001)
        server.push_cot(cot_config, "localhost", 8001)

        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
