# https://rijksmuseum.github.io/

from api_key import key
import requests
import pandas as pd



# r1 = 'https://www.rijksmuseum.nl/api/nl/collection?key=fakekey&format=json&type=schilderij&f.normalized32Colors.hex=%20%23367614'.replace('fakekey', key)
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json&type=painting&f.normalized32Colors.hex=%20%23367614'.replace('fakekey', key)
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json'.replace('fakekey', key) #this one returns count = 620338
# r1 = 'https://www.rijksmuseum.nl/api/en/collection?key=fakekey&format=json&ps=100&p=20'.replace('fakekey', key)  #returns 340479

r1 = 'https://www.rijksmuseum.nl/api/en/collection?key={}&format=json&ps=100&p={}'

count = 620338
page = 0

while count > 0:
    result = []
    count -=100
    page +=1
    print('Requesting page ',page)
    r2 = r1.format(key,page)
    print(r2)
    response = requests.get(r2)
    response_dictionary = response.json()
    art_objects = response_dictionary['artObjects']
    columns = list(art_objects[0].keys())

    for i in art_objects:
        result.append(list(i.values()))
    df = pd.DataFrame(result, columns = columns)
    df.to_csv('rijksmuseum000{}.csv'.format(page), encoding = 'utf-8')
#
#
#
#
# df = pd.DataFrame(result)
# df.to_csv('rijksmuseum.csv', encoding = 'utf-8')



#
#
# print(art_objects)
# print('\n')
#
#
# for i in art_objects:
#     print(i['webImage'])
