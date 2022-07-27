import json


with open("vol.json", 'r') as f:
    stuff = json.load(f)

stuff["games"]["ovywatch"] = 20

with open("vol.json", "w") as info:
    json.dump(stuff, info, indent=2)

