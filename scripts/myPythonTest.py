import json
import os
import sys
import numpy as np
#import urllib
import urllib2
from imdb import IMDb
import ast
import requests
import numpy as np


def exportTxt(exportFile,titleList):
    count=0
    if not os.path.isfile(exportFile):
        f=open(exportFile,"w+")
        f.close()

    with open(exportFile,'w+') as f:
        for title in titleList:
            count+=1
            f.write(title.rstrip()+'\n')

nameIds=[]

file=('m1.txt')

with open(file, 'r') as f:
    for line in f:
        nameIds.append(line.strip('\n'))


movieIds=[]
for m in nameIds:
    url='http://imdb.wemakesites.net/api/' + m + '?api_key=ed3bafe9-287b-4b42-8265-97027f2755ae'
    response = requests.get(url)
    html = response.text
    print html
    test=ast.literal_eval(html)
    if (test['status']=='success'):
        movie=test['data']['filmography']
        for url in movie:
            print 'progress'
            movieIds.append(url['info'].split('/')[4][:-1])

uniqueTitle=np.unique(movieIds)
exportTxt('t1.txt',uniqueTitle)
'''''
movies=[]
for id in movieIds:
    url1='http://www.omdbapi.com/?i='+id+'&plot=short&r=json'
    response1 = requests.get(url1)
    html1 = response1.text
    test1=ast.literal_eval(html1)
    if test1['Response']=='True':
        if test1['Type']=='movie' and (test1['Poster']!='N/A' or test1['imdbRating']!='N/A'):
            print test1
            movies.append(test1)


with open('data.json', 'w') as outfile:
    json.dump(movies, outfile)
    '''


