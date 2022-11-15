import json
from pathlib import Path
import personal as p
from typing import List, Dict, Union


def load_json(f_path: str) -> Union[List[Dict], Dict]:
  _path = Path(f_path)
  if(not _path.exists()):
    raise FileNotFoundError(f"{f_path} does not exists")

  with open(f_path, "r") as f:
    _file = f.read()
    return json.loads(_file)


p.write_csv(load_json("files/questions-data.json"), "out/questions-data.csv")
