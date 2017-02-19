import json
from pprint import pprint
import os
import numpy as np


posterIds=[]
with open('res1.json') as data_file:
    data = json.load(data_file)
    for m in data:
        if m['Plot']!='N/A':
            posterIds.append(m)
            print m['imdbID']

with open('res.json', 'w') as outfile:
    json.dump(posterIds, outfile)
