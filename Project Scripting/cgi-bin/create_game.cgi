#!/usr/bin/python3

import json
import game

spel = game.Game('woorden.txt')

with open('logs/' + spel.code + '.json', 'w') as output:
    json.dump(spel.__dict__, output)

print("Content-Type: application/json")
print()

print(json.dumps(spel.__dict__))
