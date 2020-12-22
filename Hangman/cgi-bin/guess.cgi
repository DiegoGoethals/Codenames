#!/usr/bin/python3

import json
import cgi
import game

data = json.loads(cgi.FieldStorage().getvalue('data'))

spel = game.Game(data["word"])
spel.word = data['word']
spel.progress = data['progress']
spel.mistakes_left = data['mistakes_left']
spel.winner = data['winner']
spel.selected = data['selected']
spel.code = data['code']
spel.guess(data['letter'])

with open('logs/' + spel.code + '.json', 'w') as output:
    json.dump(spel.__dict__, output)

verzenden = dict()

verzenden['selected'] = spel.selected
verzenden["winner"] = spel.winner
verzenden["progress"] = spel.progress
verzenden["mistakes_left"] = spel.mistakes_left

print("Content-Type: application/json")
print()

print(json.dumps(verzenden))