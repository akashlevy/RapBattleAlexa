import json
with open("top100raps.json") as file:
    chain = eval(file.read())
    with open("top100rapsfixed.json", "w") as file2:
        json.dump(chain, file2)
