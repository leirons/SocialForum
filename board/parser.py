import os
import requests
import json

from PIL import Image
from bs4 import BeautifulSoup

URL = 'https://33tura.ru'
FLAGI = '/flagi'
BASE_DIR = os.path.join(os.path.dirname(__file__))
FLAG_DIR = 'flags'


def check_path() -> None:
    if not os.path.exists(os.path.join(BASE_DIR, FLAG_DIR)):
        os.mkdir(FLAG_DIR)


def get_html(url) -> str:
    r = requests.get(url)
    return r.text


def get_countries(html: str) -> list:
    soup = BeautifulSoup(html, 'lxml')
    find_country = soup.find_all('tr', style='height: 15pt;')
    countries = [i.text.strip() for i in find_country]
    return countries


def get_src_img(html: str) -> list:
    soup = BeautifulSoup(html, 'lxml')
    find_img = soup.find_all('img')
    src_imgs = [i['src'] for i in find_img]
    return src_imgs


def load_picture(src: str, name: str) -> None:
    r = requests.get(URL + src, stream=True).raw

    img = Image.open(r)
    img = img.convert('RGB')
    img.resize((24, 16), Image.ANTIALIAS).save(
        f'{os.path.join(BASE_DIR, FLAG_DIR, name)}.jpg',
        'JPEG'
    )


def load_img_and_return_names(countries: list, src_imgs: list) -> list:
    names = []

    n=1
    for country, src in zip(countries, src_imgs[:-1]):
        print(f'{n}/{len(src_imgs[:-1])} запись')
        name = ''.join(country.replace('\n', ' ').strip())
        names.append(country)
        load_picture(src=src, name=name)
        n+=1
    return names


def get_json(names: list) -> None:
    pictures = sorted(list(os.walk(os.path.join(BASE_DIR, FLAG_DIR)))[0][-1])
    data = {}
    n = 1
    for name, picture in zip(names, pictures):
        name = ''.join(name.replace('\n', ' ').strip())
        picture = '{}'.format(os.path.join(BASE_DIR, FLAG_DIR, picture))

        data[n] = {
            'name': name,
            'picture': picture
        }
        n += 1
    with open('country.json', 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    html = get_html(URL + FLAGI)
    countries, src_imgs = get_countries(html), get_src_img(html)

    print(f'Создаем директорию {FLAG_DIR}')
    check_path()

    names = load_img_and_return_names(countries=countries, src_imgs=src_imgs)
    get_json(names=names)

if __name__ == '__main__':
    main()