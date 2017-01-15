import os
import sys
import numpy as np
import imdb

def fileWalker(directory,file):
    filesToScrape=[]
    for subdir, dirs, files in os.walk(directory):
        for d in dirs:
            filesToScrape.append(d)

    uniqueTitle=np.unique(filesToScrape)
    export(file,uniqueTitle)

def mergeFiles(file1,file2):
    titles=[]
    with open(file1,'r') as f1:
        for line in f1:
            titles.append(line)
    
    with open(file2,'r') as f2:
        for line in f2:
            titles.append(line)
    
    uniqueTitle=np.unique(titles)
    export(file1,uniqueTitle)
    
def readLst(directory,exportFile):
    # TODO:implement function for extracting codes from hts_cache/*.lst files
    titles=[]
    for subdir, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".lst"):
                filename=os.path.join(directory,f)
                with open(filename,'r') as listFile:
                    for line in listFile:
                        fooArray=line.split("/")
                        if fooArray[1]=="title":
                            titles.append(fooArray[2][:9])
    
    uniqueTitle=np.unique(titles)
    export(exportFile,uniqueTitle)


def export(exportFile,titleList):
    count=0
    if not os.path.isfile(exportFile):
        f=open(exportFile,"w+")
        f.close()

    with open(exportFile,'w+') as f:
        for title in titleList:
            if title.startswith("tt"):
                count+=1
                f.write(title.rstrip()+'\n')

    print count,"titles written in", exportFile

def fetchMovieInfo(titleList):
    # im=imdb.IMDb()
    # result=im.get_movie(titleCode)
    # ####im.update(result)
    # result.data
    pass

if __name__ == '__main__':
    if(sys.argv[1]=="-m"):
        mergeFiles(sys.argv[2],sys.argv[3])
    elif (sys.argv[1]=="-d"):
        files=fileWalker(sys.argv[2])
        print files
    elif (sys.argv[1]=="-l"):
        readLst(sys.argv[2],sys.argv[3])
        