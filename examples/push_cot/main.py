from atakcots import CotConfig, push_cot


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="My_Message",
        latitude=34.850132,
        longitude=137.120065
    )
        
    push_cot(cot_config, "192.168.99.169", 8001)
