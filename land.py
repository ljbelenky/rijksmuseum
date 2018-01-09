# https://rijksmuseum.github.io/

from api_key import key
# from bs4 import BeautifulSoup
# import urllib3
import requests
import pandas as pd



# r1 = 'https://www.rijksmuseum.nl/api/nl/collection?key=fakekey&format=json&type=schilderij&f.normalized32Colors.hex=%20%23367614'.replace('fakekey', key)
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json&type=painting&f.normalized32Colors.hex=%20%23367614'.replace('fakekey', key)
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json'.replace('fakekey', key) #this one returns count = 620338
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json&ps=100&p=20'.replace('fakekey', key)  #returns 340479

r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json&ps=100&p=page'.replace('fakekey', key)  #returns 340479


count = 620#338
page = 0
result = []
while count > 100:
    count -=100
    page +=1
    print('Requesting page ',page)
    r1 = r1.replace('page',str(page))
    response = requests.get(r1)
    response_dictionary = response.json()
    art_objects = response_dictionary['artObjects']
    for i in art_objects:
        result.append(list(i.values()))


df = pd.DataFrame(result)
df.to_csv('rijksmuseum.csv')



#
#
# print(art_objects)
# print('\n')
#
#
# for i in art_objects:
#     print(i['webImage'])
