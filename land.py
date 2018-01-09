# https://rijksmuseum.github.io/
from api_key import key
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import shutil
import urllib

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
    page = 5

    while True:
        print('*'*10)
        print('working on page {}'.format(page))
        print('*'*10)
        print('Requesting page ',page)
        r2 = r1.format(key,page)
        print(r2)
        response = requests.get(r2)
        response_dictionary = response.json()
        art_objects = response_dictionary['artObjects']
        for i in art_objects:
            web_link = i['links']['web']
            object_id = i['objectNumber']
            get_image(web_link, object_id)
        page +=1
        if 100*page>count: break

def get_image(web_link, object_id):
    filename = 'paintings/{}.jpg'.format(object_id)

    response = requests.get(web_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_link = soup.find('meta',{'property':'og:image'})['content']
    print(object_id)
    try:
        urllib.request.urlretrieve(img_link,filename)
    except:
        print('Some sort of error at image download')

def download_image_reqeusts(object_id):
    base_url = 'https://www.rijksmuseum.nl/en/collection/'
    # object_id = 'SK-A-389'
    filename = 'paintings/{}.jpg'.format(object_id)
    try:
        response = requests.get(base_url+object_id)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_link = soup.find('meta',{'property':'og:image'})['content']
        print(img_link)
        r = requests.get(img_link, stream = True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw,f)
    except:
        print('Some error in donwload_image_requests')


if __name__ == '__main__':
	find_download_images()
