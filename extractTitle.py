import os
import sys

def fileWalker(directory):
    filesToScrape=[]
    for subdir, dirs, files in os.walk(directory):
        for d in dirs:
            filesToScrape.append(d)

    return filesToScrape

if __name__ == '__main__':
    files=fileWalker(sys.argv[1])
    print files