import json
import os
from imdb import IMDb
import ast
import requests
import numpy as np
import time

'''
def exportTxt(exportFile,titleList):
    count=0
    if not os.path.isfile(exportFile):
        f=open(exportFile,"w+")
        f.close()

    with open(exportFile,'w+') as f:
        for title in titleList:
            count+=1
            f.write(title.rstrip()+'\n')

movieIds=[]

file=('clearIds.txt')

with open(file, 'r') as f:
    for line in f:
        movieIds.append(line.strip('\n'))

movieIds=[]
start = time.time()
for m in nameIds:
    url='http://imdb.wemakesites.net/api/' + m + '?api_key=ed3bafe9-287b-4b42-8265-97027f2755ae'
    try:
        response = requests.get(url)
        html = response.text
        print html
        test=ast.literal_eval(html)
        if (test['status']=='success'):
            movie=test['data']['filmography']
            for url in movie:
                print 'progress'
                movieIds.append(url['info'].split('/')[4][:-1])
    except:
        print "Some exception occured"
        print "Waiting.."
        time.sleep(20)
        response = requests.get(url)
        html = response.text
        print str(m)
        movieIds.append(html)
        print "Resuming download.."


uniqueTitle=np.unique(movieIds)
exportTxt('t1.txt',uniqueTitle)

posterId=[]
movies=[]
notExepted = []
start = time.time()
for id in movieIds:
    url1='data.json'#'http://www.omdbapi.com/?i=tt'+id+'&plot=short&r=json'
    try:
        response1 = requests.get(url1)
        html1 = response1.text
        test1=ast.literal_eval(html1)
        if test1['Response']=='True':
            if test1['Type']=='movie' and test1['Poster']!='N/A':
                print id
                posterId.append(id)
                movies.append(test1)
            else:
                print 'noP'
        else:
            print 'NO'
    except:
        print "Some exception occured"
        print "Waiting.."
        time.sleep(5)
        response = requests.get(url1)
        html = response.text
        print str(html)
        print "Resuming download.."


with open('data.json', 'w') as outfile:
    json.dump(movies, outfile)

with open('posterId.json', 'w+') as f:
    for p in posterId:
        f.write(p)
'''


