# ATAK_push_cots
Push Cursor on Target messages to TAK clients with attachments and other information


## Background ##
The Android Tactical Awareness Kit (ATAK) is a software platform used to enable geospatial awareness and multiuser collaboration. ATAK was originally developed by the Air Force Research Laboratory (AFRL) and is now maintained by the TAK Product Center (TPC) as a civilian application. This package exists to allow the easy sharing of markers (CoTs) to users of ATAK and other CivTAK distributions exist such as iTAK (iOS) and WinTAK (Windows).

A summary of the cursor on target schema (CoT) can be found [here](https://www.mitre.org/sites/default/files/pdf/09_4937.pdf).

For troubleshooting, create an issue or ask on the [reddit](https://www.reddit.com/r/ATAK/wiki/index) or [discord](https://discord.com/invite/xTdEcpc).


## Install ##
```bash
git clone https://github.com/kylesayrs/ATAK_push_cots
cd ATAK_push_cots
python3 -m pip install -e .
```


## Usage ##
Pushing a standard CoT message can be done using the `push_cot` function
```python
from atakcots import CotConfig, push_cot

cot_config = CotConfig(
    uid="Message",
    latitude=40.74931973338903,
    longitude=-73.96791282024928
)
    
push_cot(cot_config, "192.168.0.2")
```

Pushing CoTs which include attachments such as images must be done using `CotServer.push_cot`
```python
from atakcots import CotConfig, CotServer

cot_config = CotConfig(
    uid="Message",
    latitude=40.74931973338903,
    longitude=-73.96791282024928,
    attachment_paths="sandeot.png"
)
    
with CotServer("192.168.0.1", 8000) as server:
    server.push_cot(cot_config, "192.168.0.2")
    server.push_cot(cot_config, "192.168.0.3")
    server.push_cot(cot_config, "192.168.0.4")

    # you should keep the context alive for as long as
    # you want clients to receive the attachments
```

If you'd rather not use a context manager, you can use `start` and `stop` functions
```python
from atakcots import CotConfig, CotServer

cot_config = CotConfig(
    uid="Message",
    latitude=40.74931973338903,
    longitude=-73.96791282024928,
    attachment_paths="sandeot.png"
)

server = CotServer("192.168.0.1", 8000)
server.start()

server.push_cot(cot_config, "192.168.0.2")
server.push_cot(cot_config, "192.168.0.3")
server.push_cot(cot_config, "192.168.0.4")

# stop when clients no longer need to receive attachments
server.stop()
```

See `examples` for more use cases.
