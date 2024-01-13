# ATAK_push_cots
Push Cursor on Target messages for ATAK with attachments and other information

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


## Usage ##
Sending a standard CoT message can be done using the `push_cot` function
```python
from atakcots import CotConfig, push_cot

cot_config = CotConfig(
    uid="My_Message",
    latitude=34.850132,
    longitude=137.120065
)
    
push_cot(cot_config, "192.168.99.1", 8001)
```

Sending CoTs which include attachments such as images must be done using `CotServer.push_cot`
```python
from atakcots import CotConfig, CotServer

cot_config = CotConfig(
    uid="My_Message",
    latitude=34.850132,
    longitude=137.120065,
    attachment_paths="sandeot.png"
)
    
with CotServer("localhost", 8000) as server:
    server.push_cot(cot_config, "192.168.99.1", 8001)
    server.push_cot(cot_config, "192.168.99.2", 8001)
    server.push_cot(cot_config, "192.168.99.3", 8001)

    # you should keep the context alive for as long as
    # you want clients to receive the attachments
```

You can monitor statistics such which clients have requested attachments using `CotServer.stat`
```python
import time
from atakcots import CotConfig, CotServer

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
```

See `examples` for more use cases.


## Future work ##
1. Add file server in separate thread
2. Have file server report statistics
3. Double check manifest and message fields are necessary
4. Add tests
5. Add documentation

* Add support for additional data formats such as geojson 
