from atakcots import CotConfig, CotServer


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="Message",
        latitude=40.74931973338903,
        longitude=-73.96791282024928,
        attachment_paths="sandeot.png"
    )
        
    with CotServer("10.80.1.19", 8000) as server:
        server.push_cot(cot_config, "10.80.1.71", 4242)

        while True: pass
