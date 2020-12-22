#!/usr/bin/python3

import json
import cgi
import game

data = json.loads(cgi.FieldStorage().getvalue('data'))

spel = game.Game(data["word"])

with open('logs/' + spel.code + '.json', 'w') as output:
    json.dump(spel.__dict__, output)

print("Content-Type: application/json")
print()

print(json.dumps(spel.__dict__))
