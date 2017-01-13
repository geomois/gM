import os
import sys
import numpy as np

def fileWalker(directory):
    filesToScrape=[]
    for subdir, dirs, files in os.walk(directory):
        for d in dirs:
            filesToScrape.append(d)

    return filesToScrape

def mergeFiles(file1,file2):
    titles=[]
    with open(file1,'r') as f1:
        for line in f1:
            titles.append(line)
    
    with open(file2,'r') as f2:
        for line in f2:
            titles.append(line)
    
    uniqueTitle=np.unique(titles)
    count=0

    with open(file1,'w') as f1:
        for title in uniqueTitle:
            if title.startswith("tt"):
                count+=1
                f1.write(title)

    print count,"titles written"

if __name__ == '__main__':
    if(sys.argv>2):
        mergeFiles(sys.argv[1],sys.argv[2])
    else:
        files=fileWalker(sys.argv[1])
        print files