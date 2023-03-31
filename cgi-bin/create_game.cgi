#!/usr/bin/python3

import json
import game

play = game.Game('words.txt')

with open('logs/' + play.code + '.json', 'w') as output:
    json.dump(play.__dict__, output)

print("Content-Type: application/json")
print()

print(json.dumps(play.__dict__))
