import os
import sys
import numpy as np
import imdb
import json
import urllib2
import time
import ast

def exportTxt(exportFile,titleList):
    count=0
    if not os.path.isfile(exportFile):
        f=open(exportFile,"w+")
        f.close()

    with open(exportFile,'w+') as f:
        for title in titleList:
            count+=1
            f.write(title.rstrip()+'\n')

    print count,"titles written in", exportFile

filename=('titleIds.txt')
titles=[]
with open(filename, 'r') as listFile:
    for line in listFile:
        titles.append(line.strip('tt'))

uniqueTitle=np.unique(titles)
exportTxt('clearIds.txt',uniqueTitle)

