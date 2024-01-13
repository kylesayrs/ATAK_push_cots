from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=40.74931973338903,
        longitude=-73.96791282024928,
        attachment_paths="sandeot.png"
    )
        
    with CotServer("localhost", 8000) as server:
        #server.push_cot(cot_config, "localhost", 8001)
        #server.push_cot(cot_config, "localhost", 8001)
        server.push_cot(cot_config, "192.168.0.11", 8080)
        print("sent cot")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
