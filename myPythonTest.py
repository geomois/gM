import json
#import urllib
import urllib2
from imdb import IMDb
import ast


ia = IMDb()

person=ia.search_person('Joaquin Phoenix')

specificP=person[0].personID
print specificP
url='http://imdb.wemakesites.net/api/nm' + str(specificP) + '?api_key=ed3bafe9-287b-4b42-8265-97027f2755ae'
response = urllib2.urlopen(url)
html = response.read()
test=ast.literal_eval(html)
movie=test['data']['filmography']
movieIds=[]
for url in movie:
    movieIds.append(url['info'].split('/')[4][:-1])

print movieIds
movies=[]

for id in movieIds:
    url1='http://www.omdbapi.com/?i='+id+'&plot=short&r=json'
    response1 = urllib2.urlopen(url1)
    html1 = response1.read()
    test1=ast.literal_eval(html1)
    if test1['Type']=='movie' and (test1['Poster']!='N/A' or test1['imdbRating']!='N/A'):
        print test1
        movies.append(test1)


with open('data.json', 'w') as outfile:
    json.dump(movies, outfile)



