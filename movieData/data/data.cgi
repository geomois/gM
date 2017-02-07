#!/usr/bin/python
import json
import random


with open('res.json') as data_file:
    data = json.load(data_file)


response=random.sample(data,40)
print "Content-type: application/json\n\n"
print json.dumps(response)
