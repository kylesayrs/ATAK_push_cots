# ATAK_push_cots
Push Cursor on Target messages to TAK clients with attachments and other information


## Background ##
Android Tactical Awareness Kit (ATAK) is a software developed by the US Air Force
to assist geospatial awareness. A civilian distribution, CivTAK, can be found
[here](https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV).

Additionally, a summary of the cursor on target schema (CoT) can be found [here](https://www.mitre.org/sites/default/files/pdf/09_4937.pdf)

For troubleshooting, create an issue or ask on the [reddit](https://www.reddit.com/r/ATAK/wiki/index) or [discord](https://discord.com/invite/xTdEcpc), the community
is super friendly.


## Implementation ##
CoT messages with file attachments work by first sending a standard CoT along with
a link to a file sharing endpoint. This endpoint serves ATAK data packages, which
can be downloaded by ATAK and attached to the CoT.

Data packages are zip files containing attachments, (CoT messages if desired),
and a manifest file. Look at the implementation for more information on how
attachments are entered and how manifest files are formatted.


## Installation ##
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
    
push_cot(cot_config, "192.168.0.1")
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
    
with CotServer("localhost", 8000) as server:
    server.push_cot(cot_config, "192.168.0.1")
    server.push_cot(cot_config, "192.168.0.2")
    server.push_cot(cot_config, "192.168.0.3")

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

server = CotServer("localhost", 8000)
server.start()

server.push_cot(cot_config, "192.168.0.1")
server.push_cot(cot_config, "192.168.0.2")
server.push_cot(cot_config, "192.168.0.3")

# stop when clients no longer need to receive attachments
server.stop()
```

See `examples` for more use cases.


## TODO ##
1. Double check manifest and message fields are necessary
