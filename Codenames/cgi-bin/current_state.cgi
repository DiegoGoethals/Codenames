#!/usr/bin/python3

import json
import cgi
import os

data = json.loads(cgi.FieldStorage().getvalue('data'))

with open("logs/" + data['code'] + ".json", 'r') as dictionary:
    data = json.load(dictionary)

print("Content-Type: application/json")
print()

print(json.dumps(data))
