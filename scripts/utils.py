import os
import sys
import numpy as np
import imdb
import json
import urllib2
import time
import ast

def fileWalker(directory,file):
    filesToScrape=[]
    for subdir, dirs, files in os.walk(directory):
        for d in dirs:
            filesToScrape.append(d)

    uniqueTitle=np.unique(filesToScrape)
    exportTxt(file,uniqueTitle)

def readFile(path):
    titles=[]
    with open(path,'r') as f:
        for line in f:
            try:
                # titles.append(line[2:].strip('\n'))
                titles.append(line.strip('\n'))
            except:
                print "error"
    return titles

def mergeFiles(file1,file2):
    titles=[]
    with open(file1,'r') as f1:
        for line in f1:
            titles.append(line)
    
    with open(file2,'r') as f2:
        for line in f2:
            titles.append(line)
    
    uniqueTitle=np.unique(titles)
    exportTxt(file1,uniqueTitle)
    
def readLst(directory,exportFile):
    titles=[]
    for subdir, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".lst"):
                filename=os.path.join(directory,f)
                with open(filename,'r') as listFile:
                    for line in listFile:
                        fooArray=line.split("/")
                        if fooArray[1]=="name" or fooArray[1]=="title":
                            titles.append(fooArray[2][:9])
    uniqueTitle=np.unique(titles)
    exportTxt(exportFile,uniqueTitle)

def fetchMovieApi(titleList,exportFile):
    movieList=[]
    print "Fetching movies.."
    start = time.time()
    for i in xrange(0,len(titleList)):
        fetchUrl='http://www.omdbapi.com/?i='+titleList[i]+'&plot=short&r=json'
        try:
            response = urllib2.urlopen(fetchUrl)
            html=response.read()
            print str(i) +". "+titleList[i]
            movieList.append(html)
        except:
            print "Some exception occured"
            print "Waiting.."
            time.sleep(60)
            response = urllib2.urlopen(fetchUrl)
            html=response.read()
            print str(i) +". "+titleList[i]
            movieList.append(html)
            print "Resuming download.."

        if (i+1)%5000==0:
            print "Writing at ", str(i)
            exportJson(exportFile+"_"+str(i)+".json",movieList)
            movieList=[]
            # exportJson(exportFile,movieList)
    
    end = time.time()
    exportJson(exportFile+".json",movieList)
    print "Total time: "+str(end - start)

def fetchMovieInfo(titleList,exportFile):
    im=imdb.IMDb()
    movieList=[]
    for i in xrange(0,len(titleList)):
        result=im.get_movie(titleList[i])
        print titleList[i],"Fetched "+str(result)
        if str(result)!='':
           movieList.append(result.data)
        else:
            # print "ID does not exist",titleList[i]
            if i>=titleList[len(titleList)-1]:
                break

        if (i+1)%5000==0:
            print "Writing at ",str(titleList[i])
            movieList=cleanData(movieList)
            exportJson(str(titleList[i])+".json",movieList)
            movieList=[]

    movieList=cleanData(movieList)
    exportJson(exportFile,movieList)
    
def cleanData(movieList):
    fooList=[]
    for i in xrange(0,len(movieList)):
        fooDict=movieList[i]
        for key in fooDict:
            item=fooDict[key]
            if type(item)==list:
                tempList=[]
                for i in xrange(0,len(item)):
                    if type(item[i])!=unicode:
                        tempString=str(item[i])
                        # tempString=u''.join(item[i]).encode('UTF-8')
                    else:
                        tempString=item[i]
                    tempList.append(tempString)
                fooDict[key]=tempList
        fooList.append(fooDict)
    return fooList

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

def exportJson(exportFile,movies):
    count=0
    if not os.path.isfile(exportFile):
        f=open(exportFile,"w+")
        f.close()

    with open(exportFile,'a+') as f:
        for movie in movies:
            count+=1
            # json.dump(movie,f,sort_keys=True, indent=2)
            json.dump(movie,f)
            f.write('\n')

    print count,"titles written in", exportFile

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF8')
    if(sys.argv[1]=="-m"):
        mergeFiles(sys.argv[2],sys.argv[3])
    elif (sys.argv[1]=="-d"):
        files=fileWalker(sys.argv[2])
        print files
    elif (sys.argv[1]=="-l"):
        readLst(sys.argv[2],sys.argv[3])
    elif (sys.argv[1]=="-f"):
        codeList=np.arange(int(sys.argv[3]),6500000)
        codeList=["tt%07d"%i for i in codeList]
        # fetchMovieInfo(codeList,sys.argv[2])
        fetchMovieApi(codeList,sys.argv[2])
    elif (sys.argv[1]=="-r"):
        titles=readFile(sys.argv[2])
        fetchMovieApi(titles,sys.argv[3])
