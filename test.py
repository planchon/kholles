import json

with open("../data.json", "r") as data:
    exo = json.load(data)

print(type(exo))
