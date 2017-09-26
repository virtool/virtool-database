import json

names = list()

with open("viruses.json", "r") as f:    
    names = [virus["name"] for virus in json.load(f)]


names = sorted(names)

with open("names.txt", "w") as f:
    f.write("\n".join(names))