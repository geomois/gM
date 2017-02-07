#!/usr/bin/python
import json

posterIds=[]
with open('data.json') as data_file:
    data = json.load(data_file)



print "Content-type: application/json\n\n"
print json.dumps(data[1:4])
