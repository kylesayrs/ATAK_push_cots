from atakcots import CotConfig, push_cot


if __name__ == "__main__":
    cot_config = CotConfig(
        uid="Message",
        latitude=40.74931973338903,
        longitude=-73.96791282024928
    )

    push_cot(cot_config, "10.80.1.71")
