
import base64
import gzip
from pathlib import Path


# base64-encoded file contents
file_data = {'main.py': 'H4sIALzAVGAC/ysoyswr0cgvSM3TUErOz0vTT0osTtUvSCxKzE0tSS0q1qvMzVHS1CtKTUzR0NTkAgBBhlMoLwAAAA==', 'conf/base/parameters.yml': 'H4sIALzAVGAC/1NWKEgsSsxNLUktKtarzM3hykjNycmPBwtaKSh5gHg6CuH5RTkpikpcAF0YfLUuAAAA'}


for path, encoded in file_data.items():
    print("[Decoding] " + path)
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_bytes(gzip.decompress(base64.b64decode(encoded)))

print("*** Started to run ***")

!export PYTHONPATH=${PYTHONPATH}:${PWD}
!python main.py
