#!/usr/bin/python3

import json
import cgi
import game

data = json.loads(cgi.FieldStorage().getvalue('data'))

spel = game.Game('woorden.txt')
spel.words = data['words']
spel.red_team = data['red']
spel.blue_team = data['blue']
spel.selected = data['selected']
spel.assassin = data['assassin']
spel.neutral = data['neutral']
spel.current_player = data['current_player']
spel.code = data['code']
spel.move(data['word'])

with open('logs/' + spel.code + '.json', 'w') as output:
    json.dump(spel.__dict__, output)

verzenden = dict()

verzenden['selected'] = spel.selected
verzenden["winner"] = spel.winner
verzenden["current_player"] = spel.current_player

print("Content-Type: application/json")
print()

print(json.dumps(verzenden))
