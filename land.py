# https://rijksmuseum.github.io/
from api_key import key
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import os

def download_metadata():
    r1 = 'https://www.rijksmuseum.nl/api/en/collection?key={}&format=json&type=painting&ps=100&p={}'

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
        df.to_csv('rijksmuseum_paintings000{}.csv'.format(page), encoding = 'utf-8')

def download_image(object_id):
    base_url = 'https://www.rijksmuseum.nl/en/collection/'
    # object_id = 'SK-A-389'
    filename = 'paintings/{}.jpg'.format(object_id)
    try:
        response = requests.get(base_url+object_id)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_link = soup.find('meta',{'property':'og:image'})['content']
        print(img_link)
        urllib.request.urlretrieve(img_link,filename)
    except:
        print('Some sort of error at image download')

def get_object_ids():
    csv_files = [file for file in os.listdir() if '.csv' in file]

    object_ids = []
    for file in csv_files:
        df = pd.read_csv(file)
        if 'objectNumber' in df.columns:
            object_ids.extend(list(df.objectNumber.values))

    return object_ids

def find_download_images():
    r1 = 'https://www.rijksmuseum.nl/api/en/collection?key={}&format=json&type=painting&ps=100&p={}'

    count = requests.get(r1.format(key,0)).json()['count']
    page = 0

    while count > 0:
        count -=100
        print('*'*10)
        print('working on page {}'.format(page))
        print('*'*10)
        print('Requesting page ',page)
        r2 = r1.format(key,page)
        page +=1
        print(r2)
        response = requests.get(r2)
        response_dictionary = response.json()
        art_objects = response_dictionary['artObjects']
        columns = list(art_objects[0].keys())
        if 'objectNumber' in columns:
            for i in art_objects:
                try:
                    download_image(i['objectNumber'])
                except:
                    pass
