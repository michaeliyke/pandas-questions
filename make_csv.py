import personal as p

p.write_csv(p.load_json("files/questions-data.json"), "out/questions-data.csv")
p.write_csv(p.load_json("files/answers-data.json"), "out/answers-data.csv")
