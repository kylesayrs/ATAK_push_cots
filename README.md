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
Start the file server
```
python3 serveFiles.py
```

Place files in attachments folder (these will be zipped and served later)
```
mv <file> ./attachments/<cot_uid>/
```

Edit pushCoT.py address variables
```
# Connection to ATAK device
IP = '192.168.99.199'
PORT = 4242

# Connection to file server
SERVER_IP = '192.168.99.169' # public ip
SERVER_PORT = 8001           # file server port
```

Edit main.py to serve your needs, and send away!
```
nano main.py
python3 main.py
```

## Future work ##
* Restructure as a python package which can be better integrated into existing projects
* Implement relevant CoT parameters as arguments rather than hard-coded values
* Add support for additional data formats such as geojson 


```python
from atakcots import CotServer, CotConfig

cot_config = CotConfig(
    uid="My_Message",
    latitude=34.850132,
    longitude=137.120065,
    attachment_paths="my_image.png"
)

with CotServer("localhost", 8000, directory="/tmp", wait_req_before_close=True) as server:
    server.push_cot(cot_config, "192.168.99.169", 8001)
    server.push_cot(cot_config, "192.168.99.169", 8001)
    server.push_cot(cot_config, "192.168.99.169", 8001)
```




```python
from atakcots import CotServer, CotConfig

server = CotServer("localhost", 8000, directory="/tmp")
server.start()
cot_config = CotConfig(
    uid="My_Message",
    latitude=34.850132,
    longitude=137.120065,
    attachment_paths="my_image.png"
)
server.push_cot(cot_config, "192.168.99.169", 8001)

# once the mission is finished
server.close()
```


```python
from atakcots import push_cot

cot_config = CotConfig(
    uid="My_Message",
    latitude=34.850132,
    longitude=137.120065,
)

push_cot(cot_config, "192.168.99.169", 8001)
```
