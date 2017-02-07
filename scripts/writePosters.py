import json
from pprint import pprint
import os
import numpy as np


posterIds=[]
with open('data.json') as data_file:
    data = json.load(data_file)
    for m in data:
        if m['Poster']!='N/A':
            posterIds.append(m)
            print m['imdbID']

with open('res.json', 'w') as outfile:
    json.dump(posterIds, outfile)
