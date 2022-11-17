from typing import Dict, List, Union
import typo
import uuid
import personal as p

ROWS: List[Dict] = p.load_json("files/questions-data.json")

print("MODIFYING DATA VALUES")
row: Dict

for index, row in enumerate(ROWS):
  UUID: uuid.UUID = uuid.uuid4()
  mis_type = typo.StrErrer(row["question"], seed=2)

  ROWS[index]["question"] = mis_type.missing_char().result
  ROWS[index]["question_id"] = ROWS[index]["id"]
  ROWS[index]["id"] = f"{UUID}"

p.write_csv(ROWS, "out/questions-data-typos.csv")
p.write_json(ROWS, "files/questions-data-typos.json")

print("ALL DONE!")
