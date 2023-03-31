#!/usr/bin/python3

import json
import cgi
import game

data = json.loads(cgi.FieldStorage().getvalue('data'))

play = game.Game('woorden.txt')
play.words = data['words']
play.red_team = data['red']
play.blue_team = data['blue']
play.selected = data['selected']
play.assassin = data['assassin']
play.neutral = data['neutral']
play.current_player = data['current_player']
play.code = data['code']
play.end_turn()

with open('logs/' + play.code + '.json', 'w') as output:
    json.dump(play.__dict__, output)

send = dict()

send['current_player'] = play.current_player

print("Content-Type: application/json")
print()

print(json.dumps(send))
