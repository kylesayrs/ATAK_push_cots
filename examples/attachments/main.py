from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="Message",
        latitude=40.74931973338903,
        longitude=-73.96791282024928,
        attachment_paths="sandeot.png"
    )
        
    with CotServer("localhost", 8000) as server:
        server.push_cot(cot_config, "192.168.0.1")
        server.push_cot(cot_config, "192.168.0.2")
        server.push_cot(cot_config, "192.168.0.3")

        try:
            while True: pass
        except KeyboardInterrupt:
            pass
